# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的调度器

import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        print('\033[1;30;42m 测试器准备就绪 \033[0m')
        while True:
            time.sleep(cycle)
            tester.run()

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('\033[1;30;42m 开始抓取代理 \033[0m')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        print("\033[1;30;42m 开始运行API \033[0m")
        app.run(API_HOST, API_PORT)

    def run(self):
        print('\033[1;30;41m 代理池开始运行 \033[0m')
        if API_ENABLED:  # 启动API
            api_process = Process(target=self.schedule_api)
            api_process.start()

        if GETTER_ENABLED:  # 启动获取器
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED:  # 启动检测器
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
