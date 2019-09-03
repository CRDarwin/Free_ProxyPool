# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的代理获取器和上线检测器


from proxypool.crawler import Crawler
from proxypool.db import MonClient
from proxypool.setting import *
import sys

class Getter():
    def __init__(self):
        self.mongo = MonClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.mongo.db.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('\033[1;30;44m 获取器开始执行 \033[0m')
        if not self.is_over_threshold():
            print("\033[1;30;44m 没有达到上限！ \033[0m")
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.mongo.add(proxy)
