from flask import Flask, g, request, render_template

from proxypool.db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('ledt.html')


@app.route('/random', methods=['post','get'])
def get_proxy():
    conn = get_conn()
    try:
        data = dict(
        number = 160 if request.args.get("number")== None else int(request.args.get("number")),
        type =  request.args.get('type'),
        detection =  request.args.get('detection'),
        )
        limit = 10 if request.args.get("limit")== None else int(request.args.get("limit"))
    except:
        return "请求的URL错误！"
    for key in list(data.keys()):
        if not data.get(key):
            del data[key]
    ip_list = conn.randoms(querys = data, limit=limit)
    return ip_list


@app.route('/delete', methods=['post','get'])
def delete_proxy():
    conn = get_conn()
    try:
        data = dict(
        iport=request.args.get('proxy'),
        type = request.args.get('type'),
        detection = request.args.get('detection'),
        pid =1  if not request.args.get("pid")== None and -1<int(request.args.get("pid"))<2 else int(request.args.get("pid"))
        )
    except:
        return "请求的URL错误！"
    for key in list(data.keys()):
        if not data.get(key):
            del data[key]
    ip_list = conn.deleted(data=data)
    return ip_list

@app.route('/messages')
def messages():
    conn = get_conn()
    data = conn.message()
    return render_template('message.html' ,labels = ["细分","type", "detection", "count"], subdivide= data[0], labelss = ["分类","", "types", "count"],classify= data[1],usable =  data[2],total =  data[3])



if __name__ == '__main__':
    app.run()
