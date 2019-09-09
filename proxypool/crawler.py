# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的获取IP代理

import datetime
import re
import time
from lxml import etree
from proxypool.utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('\033[1;0;96m成功获取到代理\033[0m', proxy)
            proxies.append(proxy)
        return proxies

    ##########################################################
    #
    #               定义的代理网站规则
    #
    ##########################################################

    # 89IP网站
    def crawl_89ip(self, page_count=15):
        try:
            start_url = 'http://www.89ip.cn/index_{}.html'
            urls = [start_url.format(page) for page in range(1, page_count + 1)]
            for url in urls:
                html = get_page(url)
                if html:
                    doc = pq(html)
                    trs = doc('.layui-row .layui-col-md8 .fly-panel .layui-form .layui-table  tbody tr').items()
                    for tr in trs:
                        ip = tr.find('td:nth-child(1)').text()
                        port = tr.find('td:nth-child(2)').text()
                        yield ':'.join([ip, port])
                else:
                    print("\033[1;31;40m 89IP网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                    return 0
        except:
            print("\033[1;41;97m 89IP网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 蚂蚁代理网站
    def crawl_mayidaili(self):
        try:
            d1 = datetime.datetime(2018, 12, 31)
            year = int(time.strftime("%Y", time.localtime()))
            mouth = int(time.strftime("%m", time.localtime()))
            day = int(time.strftime("%d", time.localtime()))
            d2 = datetime.datetime(year, mouth, day)
            start = (d2 - d1).days
            for i in range((1325 + (start)), 1325 + start + 1):
                html = get_page("http://www.mayidaili.com/share/view/{name}/".format(name=i))
                if html:
                    doc = pq(html)
                    iptables = doc('body > div:nth-child(4) > p').text()
                    iptable_list = iptables.split("#")
                    for i in iptable_list:
                        if not i.isalpha():
                            result = re.search('(\d+)', i)
                            start = result.start()
                            ips = i[start:]
                            yield ips.replace(' ', '')
                        else:
                            pass
                else:
                    print("\033[1;31;40m 蚂蚁代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                    return 0
        except:
            print("\033[1;41;97m 蚂蚁代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # IP海代理网站
    def crawl_iphai(self):
        try:
            start_url = 'http://www.iphai.com/'
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')
            else:
                print("\033[1;31;40m IP海代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m IP海代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 无忧代理网站
    def crawl_data5u(self):
        try:
            start_url = 'http://www.data5u.com/'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
                'Host': 'www.data5u.com',
                'Referer': 'http://www.data5u.com/free/index.shtml',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            }
            html = get_page(start_url, options=headers)
            if html:
                ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
                re_ip_address = ip_address.findall(html)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    yield result.replace(' ', '')
            else:
                print("\033[1;31;40m 无忧代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m 无忧代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # crossincode代理网站
    def crawl_crossincode(self):
        try:
            url = "http://lab.crossincode.com/proxy/"
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc(".container-fluid .row .col-md-10 .root-index-block .proxy-index-table tr").items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
            else:
                print("\033[1;31;40m crossincode代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m crossincode代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 够搬家代理网站
    def crawl_goubanjia(self):
        try:
            url = "http://www.goubanjia.com/"
            html = get_page(url)
            if html:
                tree = etree.HTML(html)
                proxy_list = tree.xpath('//td[@class="ip"]')
                # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
                # 需要过滤掉<p style="display:none;">的内容
                xpath_str = """.//*[not(contains(@style, 'display: none'))
                                and not(contains(@style, 'display:none'))
                                and not(contains(@class, 'port'))
                                ]/text()
                            """
                for each_proxy in proxy_list:
                    try:
                        # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                        ip_addr = ''.join(each_proxy.xpath(xpath_str))
                        port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                        yield '{}:{}'.format(ip_addr, port)
                    except:
                        pass
            else:
                print("\033[1;31;40m 够搬家代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m 够搬家代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # IP代理库代理网站
    def crawl_jiangxianli(self):
        try:
            url = 'http://ip.jiangxianli.com/?page=1'
            html = get_page(url)
            if html:
                html_tree = etree.HTML(html)
                tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
                for tr in tr_list:
                    yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]
            else:
                print("\033[1;31;40m IP代理库代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0

        except:
            print("\033[1;41;97m IP代理库代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 极速代理网站
    def crawl_superfastip(self, page_count=10):
        try:
            url_list = ["http://www.superfastip.com/welcome/freeip/{}".format(page) for page in
                        range(1, page_count + 1)]
            for url in url_list:
                html = get_page(url)
                if html:
                    html_tree = etree.HTML(html)
                    ip_list = html_tree.xpath("/html/body/div[3]/div/div/div[2]/div/table/tbody//tr/td[1]/text()")
                    port_list = html_tree.xpath("/html/body/div[3]/div/div/div[2]/div/table/tbody//tr/td[2]/text()")
                    ip_lists = zip(ip_list, port_list)
                    for ip in ip_lists:
                        yield ":".join(ip)
                else:
                    print("\033[1;31;40m 极速代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                    return 0
        except:
            print("\033[1;41;97m 极速代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 小舒代理网站
    def crawl_xsdaili(self):
        try:
            html = get_page('http://www.xsdaili.com/')
            if html:
                html_tree = etree.HTML(html)
                url_lists = list(html_tree.xpath('//div[@class="title"]/a/@href'))[:2]
                for url_list in url_lists:
                    htmls = get_page('http://www.xsdaili.com' + url_list)
                    if htmls:
                        htmlss = etree.HTML(htmls)
                        result = htmlss.xpath("//div[@class='cont']/text()")
                        for ip_list in result[:-1]:
                            ip = str(ip_list).replace("\t", "").replace("\r", "").replace("\n", "").split("@")
                            yield ip[0]
                    else:
                        print("\033[1;31;40m 小舒代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                        return 0
            else:
                print("\033[1;31;40m 小舒代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m 小舒代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 神鸡代理网站
    def crawl_shenjidaili(self):
        try:
            html = get_page('http://www.shenjidaili.com/open/')
            if html:
                html_tree = etree.HTML(html)
                url_lists = html_tree.xpath('//div[@class="tab-pane fade p-3"]/table/tr/td[1]/text()')[1:]
                del url_lists[51]
                del url_lists[50]
                for url_list in url_lists:
                    yield url_list
            else:
                print("\033[1;31;40m 神鸡代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m 神鸡代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 泥马代理网站
    def crawl_nimadaili(self):
        urls = ["http://www.nimadaili.com/http/{}/", "http://www.nimadaili.com/gaoni/{}/", "http://www.nimadaili.com/https/{}/"]
        try:
            for url in urls:
                for page in range(100):
                    html = get_page(url.format(str(page)))
                    if html:
                        html_tree = etree.HTML(html)
                        for ip in html_tree.xpath('/html/body/div/div[1]/div[2]/table/tbody/tr/td[1]/text()'):
                            yield ip
                    else:
                        print("\033[1;31;40m 泥马代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                        return 0
                    time.sleep(2)
        except:
            print("\033[1;41;97m 泥马代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    ##########################################################
    #
    #    过期代理（请检测是否能进入网站，再提取出来使用）
    #
    ##########################################################
    '''
# ip3366代理网站接口
    def crawl_ip3366(self):
        try:
            ip_url = "http://ged.ip3366.net/api/?key=20180728102555601&getnum=3000&proxytype=01"
            html = get_page(ip_url)
            if html:
                ip_list = html.rstrip("\r\n").split("\r\n")
                for i in ip_list:
                    yield i
            else:
                print("\033[1;31;40m IP3366网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m IP3366网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 快代理网站
    def crawl_kuaidaili(self):
        try:
            for i in range(1, 21):
                start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
                html = get_page(start_url)
                if html:
                    ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                    re_ip_address = ip_address.findall(html)
                    port = re.compile('<td data-title="PORT">(.*?)</td>')
                    re_port = port.findall(html)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')
                else:
                    print("\033[1;31;40m 快代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                    return 0
                time.sleep(1)
        except:
            print("\033[1;41;97m 快代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

    # 站大爷代理网站
    def crawl_zdaye(self):
        try:
            start_url = 'http://ip.zdaye.com/dayProxy.html'
            headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Referer': 'http://ip.zdaye.com/dayProxy/2019/7/1.html',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            response = get_page(start_url, options=headers)
            if response:
                html = etree.HTML(response)
                url_lists = map((lambda x: "http://ip.zdaye.com" + x),
                                html.xpath('//*[@id="J_posts_list"]/div/div/h3/a/@href'))
                for url_list in url_lists:
                    responses = get_page(url_list, options=headers)
                    if responses:
                        html = etree.HTML(responses)
                        ip_lists = html.xpath('//*[@id="J_posts_list"]/div[3]/text()')
                        for ip_list in ip_lists:
                            ip = str(ip_list).split("@")
                            yield ip[0]
                        time.sleep(2)
                    else:
                        print("\033[1;31;40m 站大爷代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
            else:
                print("\033[1;31;40m 站大爷代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                return 0
        except:
            print("\033[1;41;97m 站大爷代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0

 # 西刺代理网站
    def crawl_xicidaili(self):
        try:
            url_list = [
                'http://www.xicidaili.com/nn/',  # 高匿
                'http://www.xicidaili.com/nt/',  # 透明
            ]
            for each_url in url_list:
                for i in range(1, 21):
                    page_url = each_url + str(i)
                    html = get_page(page_url)
                    if html:
                        tree = etree.HTML(html)
                        proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                        for proxy in proxy_list:
                            try:
                                yield ':'.join(proxy.xpath('./td/text()')[0:2])
                            except Exception as e:
                                pass
                    else:
                        print("\033[1;31;40m 西刺代理网站  ---->  爬取网站为空已准备跳过！ \033[0m")
                        return 0
                    time.sleep(5)
        except:
            print("\033[1;41;97m 西刺代理网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
            return 0


'''
