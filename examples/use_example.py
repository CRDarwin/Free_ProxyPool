import random

import requests

# 代理池的操作类
class ipproxy():
    # 可在index页面查看具体参数信息
    def __init__(self, type=None, detection=None,limit=None, formats= None, order=None, splits=None):
        """
        :param type:  代理的检测类型
        :param detection: 代理的检测站点
        :param limit: 代理的获取数量
        :param formats: 代理的输出格式
        :param order: 代理的排列顺序
        :param splits: 代理的分隔符
        """
        self.type = type
        self.detection = detection
        self.limit = limit
        self.formats = formats
        self.order = order
        self.splits = splits
        self._ip_list = set({})

    def init_data(self, data):
        for key in list(data.keys()):
            if not data.get(key):
                del data[key]
        return data

    def get_proxy(self):    #获取代理
        params = {
            'type' : self.type,           # 请求的IP类型     （可选参数，默认为：""）
            'detection' : self.detection,      # 请求的测试网站   （可选参数，默认为：""）
            'limit' : self.limit ,           # 每次获取的IP数   （可选参数，默认为：10）
            'formats' : self.formats,
            "order" : self.order,
            "splits": self.splits
        }
        response = requests.get('http://127.0.0.1:55555/ged',params=self.init_data(params))
        print(response.url)
        if response.status_code == 200:
            return response.text.split(self.splits)
        print(response.status_code)
        print(response.text)
        return exit()


    def delete_proxy(self, porxy):  #删除代理
        try:
            self._ip_list.remove(porxy)
            params = {
                'proxy': porxy,                     # 需要删除的IP     （必填参数）
                'type': self.type,                  # 请求的IP类型     （可选参数，默认为：""）
                'detection': self.detection,        # 请求的测试网站   （可选参数，默认为：""）
            }
            response = requests.get('http://127.0.0.1:55555/del', params=params)
            print(response.url)
            print(response.text)
        except:pass

    def acquire_proxy(self):    #对获取代理的操作
        if len(self._ip_list) <= 0:
            self._ip_list = self._ip_list | set(self.get_proxy())
        print(self._ip_list)
        return random.choice(list(self._ip_list))





ip = ipproxy(type="http", detection="mohurd", limit=10,formats="text", order=0, splits="\r\n" )
