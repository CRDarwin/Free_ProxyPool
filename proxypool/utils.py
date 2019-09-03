# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  获取被爬取网站的页面信息

import requests

base_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}


def get_page(url, options=None):
    """
    抓取代理
    :param url: 爬取IP的URL
    :param options: 请求头参数
    :return:
    """
    options = {} if options is None else options
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            print("\033[1;30;47m 抓取到内容！ \033[0m")
            return response.text
        else:
            return 0
    except:
        return 0
