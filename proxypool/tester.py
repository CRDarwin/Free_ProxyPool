# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  对IP进行检测


import asyncio
import aiohttp
import time
import sys

from proxypool.db import MonClient

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.setting import *


class Tester(object):
    def __init__(self):
        self.mongo = MonClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    async def test_single_proxy(self, proxys, test_url):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        proxy = proxys["iport"]
        numbers = proxys["number"]
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                start_time = time.time()
                async with session.get(test_url, proxy=real_proxy, headers=self.headers, timeout=15, allow_redirects=False) as response:
                    end_time = time.time()
                    if response.status in VALID_STATUS_CODES:  # 判断代理是否可用
                        ping = end_time - start_time
                        detection = test_url.split(".")[1]
                        if numbers != INITIAL_SCORE:
                            print("代理可用_______________" + proxy + "_______________" + str(numbers))
                            self.mongo.db.update({"iport": proxy, "pid": DOT_PID}, {"$set": {'number': INITIAL_SCORE}})

                        nums = list(self.mongo.db.find({"iport": proxy, "type": str(test_url).split(":")[0], "detection": detection, "pid": DTC_PID},
                                                       {"number": 1, "_id": 0}))

                        if len(nums) != 0 and nums[0]["number"] != MAX_SCORE:  # 判断可用代理是否存在并且分数是否是最大值，否则更新
                            print("代理可用 " + proxy + " 分数为 " + str(nums[0]["number"]) + "进行更新")
                            self.mongo.db.update({"iport": proxy, "type": str(test_url).split(":")[0], "detection": detection, "pid": DTC_PID},
                                                 {"$set": {"number": MAX_SCORE, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}})
                        else:
                            self.mongo.add(proxy, score=MAX_SCORE, type=str(test_url).split(":")[0], detection=detection, ping=ping, pid=DTC_PID)
                            print("代理可用 " + proxy + str(str(test_url).split(":")[0]))
                    else:
                        self.mongo.decrease(proxy)
                        print('请求响应码不合法 ', response.status, 'IP', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.mongo.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('\033[1;30;44m 测试器开始运行 \033[0m')
        try:
            count = list(self.mongo.db.aggregate([{"$match": {"pid": {"$eq": 0}}}, {"$group": {"_id": None, "count": {"$sum": 1}}}]))[0]["count"]
            print('\033[1;44;31m 当前剩余 \033[0m', "\033[1;30;41m {} \033[0m".format(count), '\033[1;44;31m 个代理 \033[0m')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.mongo.batch(start, stop)
                for test_url in TEST_URL:
                    print("________测试UR_________  "+test_url)
                    loop = asyncio.get_event_loop()
                    tasks = [self.test_single_proxy(proxy, test_url) for proxy in test_proxies]
                    loop.run_until_complete(asyncio.wait(tasks))
                    sys.stdout.flush()
                time.sleep(3)
        except Exception as e:
            print('测试器发生错误', e.args)
            time.sleep(5)
