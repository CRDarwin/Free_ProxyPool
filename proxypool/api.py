# -*- coding: utf-8 -*-
# @Author  : Darwin
# @project : 代理池
# @File    : main.py
# @Time    : 2019/8/7 8:52
# @Software: PyCharm
# @Wechat Contact:  HTTP/HTTPS代理池的API接口
import json
from urllib.parse import urlencode

from flask import Flask, g, request, render_template

from proxypool.db import MonClient, API_HOST, API_PORT

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'MongoClient'):
        g.mongo = MonClient()
    return g.mongo


# 首页信息
@app.route('/')
def index():
    conn = get_conn()
    data = conn.message()
    return render_template('./index.html', subdivide=data[0], classify=data[1], available_quantity=data[2],
                           quantity_to_be_detected=str(int(data[3]) - int(data[2])), total=data[3], type=data[4], det=data[5])


# 获取链接API
@app.route('/api')
def api():
    data = dict(
        type=request.args.get('type', ),
        detection=request.args.get('detection'),
        limit=request.args.get('limit'),
        formats=request.args.get('formats'),
        order=request.args.get('order'),
        splits=request.args.get('splits')
    )
    for key in list(data.keys()):
        if not data.get(key):
            del data[key]
    url = (request.url).split("api")[0] + "ged?" + urlencode(data)
    return url


# 代理删除API
@app.route('/del', methods=['post', 'get'])
def delete_proxy():
    conn = get_conn()
    data = dict(
        iport=request.args.get('proxy'),
        type=request.args.get('type'),
        detection=request.args.get('detection'),
        pid=1)
    for key in list(data.keys()):
        if not data.get(key):
            del data[key]
    if len(set(data).symmetric_difference({"iport", "type", "detection", "pid"})) == 0:
        return conn.reduce_value(data)
    return "删除时的参数键错误！", 401


@app.route('/ged', methods=['post', 'get'])
def get_proxy():
    print(request.args.to_dict())
    return ged(request.args.to_dict())


def ged(dicts):
    conn = get_conn()
    if set(dicts.keys()).issubset(["number", "type", "detection", "limit", "formats", "splits", "order"]):
        if "number" in dicts.keys() and dicts["number"].isdigit() and int(dicts["number"]) > 0: dicts["number"] = int(dicts["number"])
        if "limit" in dicts.keys():
            if dicts["limit"].isdigit() and int(dicts["limit"]) > 0:
                limit = int(dicts["limit"])
                dicts.pop("limit")
            else:
                limit = 10
                dicts.pop("limit")
        else:
            limit = 10
        if "order" in dicts.keys():
            if int(dicts["order"]) in [-1, 0, 1]:
                order = int(dicts["order"])
                dicts.pop("order")
            else:
                order = 0
                dicts.pop("order")
        else:
            order = 0
        if "formats" in dicts.keys():
            if dicts["formats"] in ["text", "json"]:
                formats = dicts["formats"]
                dicts.pop("formats")
            else:
                formats = "text"
                dicts.pop("formats")
        else:
            formats = "text"
        if "splits" in dicts.keys():
            splits = dicts["splits"]
            dicts.pop("splits")
        else:
            splits = "\r\n"
        get_ips = conn.get_proxy(querys=dicts, limit=limit, formats=formats, splits=splits, order=order)
        if formats == "json":
            return json.dumps({"ip": list(get_ips)}, ensure_ascii=False)
        else:
            return get_ips
    else:
        return "输入的参数键有错误！"


if __name__ == '__main__':
    app.run()
