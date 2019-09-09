# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的数据库链接及API操作

import pymongo

from proxypool.setting import *
import re
import time


class MonClient(object):
    def __init__(self, host=MONGO_HOST, port=MONGO_PORT, password=MONGO_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = pymongo.MongoClient(host=host, port=port, password=password).get_database(MONGO_DB).get_collection(MONGO_TABLE)

    def add(self, proxy, score=INITIAL_SCORE, type=None, detection=None, ping=0.0, pid=DOT_PID):
        """
        添加代理，设置分数为入库值或添加代理为最大值
        :param proxy:       代理
        :param score:       分数
        :param type:        类型
        :param detection:   检测网站
        :param ping:        延迟
        :param pid:         是否可用
        # :param timestamp:   入库时间
        :return:    添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return 0
        if self.db.find({"iport": proxy, "type": type, "detection": detection, "pid": pid}).count() == 0:
            datas = dict(iport=proxy, number=score, type=type, detection=detection, ping=ping, pid=pid,
                         timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return self.db.insert(datas)

    def batch(self, start, stop):
        """
        批量获取代理，用来提取待检测IP
        :param start:       开始索引
        :param stop:        结束索引
        :return:    代理列表
        """
        return list(self.db.find({"pid": DOT_PID}, {"iport": 1, "number": 1, "_id": 0}).sort([("timestamp", 1)]).limit((int(stop) - int(start))).skip(
            start))

    def decrease(self, proxy):
        """
        对代理进行检测，不通过值减一分，小于最小值则删除
        :param proxy:       代理
        :return:    修改后的代理分数
        """
        score = self.db.find({"iport": proxy, "pid": DOT_PID}, {"number": 1, "_id": 0})[0]["number"]
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.update({"iport": proxy, "pid": DOT_PID}, {"$set": {'number': score - 1}})
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.remove_ip({"iport": proxy, "pid": 0})

    def remove_ip(self, data):
        """
        删除被检测代理小于最小值
        :param data:        字典，被删除的代理IP与pid
        :return: 删除IP
        """
        whether = self.db.remove(data)
        if whether["n"] != 0:
            return "删除成功！", 200
        else:
            return "删除失败！", 200

    def reduce_value(self, data):
        """
        对验证过的代理，进行删除或者减少
        :param data:     代理进行验证的信息
        :return:
        """
        try:
            if MAX_SCORE >= list(self.db.find(data, {"number": 1, "_id": 0}))[0]['number'] > (MAX_SCORE - REMOVE_SCORE):
                self.db.update(data, {"$inc": {"number": -1}})
                return "更新成功！"
            else:
                return self.remove_ip(data)
        except:
            return "代理池中无此代理或代理参数值错误！", 401

    def message(self):
        subdivide = list(self.db.aggregate(
            [{"$match": {"type": {"$ne": None}}}, {"$group": {"_id": {"type": "$type", "detection": "$detection"}, "count": {"$sum": 1}}},
             {"$project": {"_id": 1, "count": 1}}, ]))
        classify = list(self.db.aggregate([{"$match": {"type": {"$ne": None}}}, {"$group": {"_id": {"type": "$type", }, "count": {"$sum": 1}}},
                                           {"$project": {"_id": 1, "count": 1}}, ]))
        usable = str(self.db.find({"type": {"$ne": None}}).count())
        total = str(self.db.find().count())
        subdivide = list(map((lambda x: (x["_id"]["type"], x["_id"]["detection"], x["count"])), subdivide))
        classify = list(map((lambda x: (x["_id"]["type"], x["count"])), classify))
        type = set(map(lambda x: x[0], subdivide))
        detection = set(map(lambda x: x[1], subdivide))
        return subdivide, classify, usable, total, type, detection

    def get_proxy(self, querys, limit, formats, order, splits):
        """

        :param querys:
        :param limit:
        :param formats:
        :param order:
        :param splits:
        :return:
        """
        if formats == "text" and order == 0:  # 返回格式为text， 排序方式为随机
            data = list(map((lambda x: x["iport"]),
                            self.db.aggregate([{"$match": querys}, {"$project": {"_id": 0, "iport": 1}}, {'$sample': {'size': limit}}])))
            if len(data) > 0:
                return splits.join(data)
            return "代理池枯竭或者参数错误！", 405
        if formats == "text" and order == 1:  # 返回格式为text， 排序方式为升序
            data = list(map((lambda x: x["iport"]),
                            self.db.aggregate([{"$match": querys}, {"$sort": {"ping": 1}}, {"$project": {"_id": 0, "iport": 1}}, {"$limit": limit}])))
            if len(data) > 0:
                return splits.join(data)
            return "代理池枯竭或者参数错误！", 405
        if formats == "text" and order == -1:  # 返回格式为text， 排序方式为降序
            data = list(map((lambda x: x["iport"]), self.db.aggregate(
                [{"$match": querys}, {"$sort": {"ping": -1}}, {"$project": {"_id": 0, "iport": 1}}, {"$limit": limit}])))
            if len(data) > 0:
                return splits.join(data)
            return "代理池枯竭或者参数错误！", 405
        if formats == "json" and order == 0:  # 返回格式为json， 排序方式为随机
            data = list(self.db.aggregate(
                [{'$match': querys}, {"$project": {"_id": 0, "iport": 1, "type": 1, "detection": 1, "ping": 1, "timestamp": 1}},
                 {'$sample': {'size': limit}}]))
            if len(data) > 0:
                return data
            return "代理池枯竭或者参数错误！", 405
        if formats == "json" and order == 1:  # 返回格式为json， 排序方式为升序
            data = list(self.db.aggregate(
                [{'$match': querys}, {"$project": {"_id": 0, "iport": 1, "type": 1, "detection": 1, "ping": 1, "timestamp": 1}},
                 {"$sort": {"ping": 1}},
                 {"$limit": limit}]))
            print(data)
            if len(data) > 0:
                return data
            return "代理池枯竭或者参数错误！", 405
        if formats == "json" and order == -1:  # 返回格式为json， 排序方式为降序
            data = list(self.db.aggregate(
                [{'$match': querys}, {"$project": {"_id": 0, "iport": 1, "type": 1, "detection": 1, "ping": 1, "timestamp": 1}},
                 {"$sort": {"ping": -1}},
                 {"$limit": limit}]))
            if len(data) > 0:
                return data
            return "代理池枯竭或者参数错误！", 405
