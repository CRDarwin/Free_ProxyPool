import pymongo

from proxypool.setting import MONGO_PORT, MONGO_HOST, MONGO_PASSWORD, MONGO_DB, MONGO_TABLE, INITIAL_SCORE, MIN_SCORE
import re


class RedisClient(object):
    def __init__(self, host=MONGO_HOST, port=MONGO_PORT, password=MONGO_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = pymongo.MongoClient(host=host, port=port, password=password).get_database(MONGO_DB).get_collection(MONGO_TABLE)

    def add(self, proxy, score=INITIAL_SCORE, type=None, detection=None, ping=0.0, pid=0):
        """
        添加代理，设置分数为平均值或添加代理为最大值
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return 0
        if self.db.find({"iport": proxy, "type": type, "detection": detection, "pid": pid}).count() == 0:
            datas = dict(iport=proxy, number=score, type=type, detection=detection, ping=ping, pid=pid)
            return self.db.insert(datas)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        ip_list = self.db.find({"pid": 0}, {"iport": 1, "_id": 0}).limit((int(stop) - int(start))).skip(start)
        return list(map((lambda x: x["iport"]), ip_list))

    def deleted(self,data={}):
        """
        删除指定IP内容
        :param proxy: 代理IP
        :param type: IP类型  ["http" , "https"]
        :param detection: 检测网点   baidu , ip3366
        :param pid: IP是否可用  [0,1]
        :return: 删除IP
        """
        options = dict({"pid":0}, **data)
        print(options)
        whether = self.db.remove(options)
        if whether["n"] ==1:
            return "删除成功！"
        else:return "删除失败！"

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.find({"iport": proxy, "pid": 0}, {"number": 1, "_id": 0})[0]["number"]
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.update({"iport": proxy, "pid": 0}, {"$set": {'number': score - 1}})
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.deleted({"iport":proxy})

    def randoms(self, querys = {}, limit=10):
        """
        获取
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        querys = dict({"pid":1}, **querys)

        ips = list(map((lambda x:x["iport"]), self.db.find(querys, {"iport":1, "_id":0}).sort([("ping",1)]).limit(limit)))
        ips = "\r\n".join(ips)
        return ips

    def message(self):
        subdivide = list(self.db.aggregate([{"$match": {"type": {"$ne": None}}},{"$group": {"_id": {"type": "$type","detection": "$detection"},"count": {"$sum": 1} } },{"$project": {"_id": 1, "count": 1}},]))
        classify = list(self.db.aggregate([{"$match": {"type": {"$ne": None}}},{"$group": { "_id": { "type": "$type", },"count": {"$sum": 1} } },{"$project": {"_id": 1, "count": 1}},]))
        usable = str(self.db.find({"type":{"$ne":None}}).count())
        total = str(self.db.find().count())
        subdivide = list(map((lambda x:(x["_id"]["type"], x["_id"]["detection"],x["count"])), subdivide))
        classify = list(map((lambda x:(x["_id"]["type"],x["count"])), classify))

        return subdivide, classify, usable, total

if __name__ == '__main__':
    conn = RedisClient()
    # ss = conn.deleted(data={"iport":"49.156.35.230:8080", "type":"http","detection":"mohurd","pid":1})
    # print(ss)

