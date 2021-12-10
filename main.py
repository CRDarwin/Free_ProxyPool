# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的启动接口

import sys
import io

from proxypool.scheduler import Scheduler
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        sss
        s = Scheduler()
        s.run()
    except: main()

if __name__ == '__main__':
    main()
