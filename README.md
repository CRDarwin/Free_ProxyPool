# 爬虫IP代理池(未开发完成)

```
______                        ______             _
| ___ \_                      | ___ \           | |
| |_/ / \__ __   __  _ __   _ | |_/ /___   ___  | |
|  __/|  _// _ \ \ \/ /| | | ||  __// _ \ / _ \ | |
| |   | | | (_) | >  < \ |_| || |  | (_) | (_) || |___
\_|   |_|  \___/ /_/\_\ \__  |\_|   \___/ \___/ \_____\
                       __ / /
                      /___ /
```

##### [介绍文档](https://github.com/CRDarwin/Free_ProxyPool/blob/master/docx/introduce.md)

- 支持版本: ![](https://img.shields.io/badge/Python-3.x-blue.svg)

### 下载安装

- 下载源码:

```shell
git clone https://github.com/CRDarwin/Free_ProxyPool.git

或者直接到 https://github.com/CRDarwin/Free_ProxyPool.git 下载zip文件
```

- 安装依赖:

```shell
pip install -r requirements.txt
```

- 配置proxypool/setting.py:

```shell
# proxypool/setting.py 为项目配置文件

# MongoDB数据库配置信息
MONGO_HOST = 'localhost'            # MongoDB数据库地址
MONGO_PORT = 27017                  # MongoDB端口
MONGO_PASSWORD = None               # MongoDB密码，如无填None
MONGO_DB = 'proxy'                  # MongoDB数据库名称
MONGO_TABLE = 'proxies'            # MongoDB数据集合

# 代理中pid的类型
DTC_PID = 1                         # 可用IP
DOT_PID = 0                         # 未检测IP

# 代理分数
MAX_SCORE = 160                     # 可用代理分数
MIN_SCORE = 60                      # 移除代理分数
INITIAL_SCORE = 100                 # 进库代理分数

VALID_STATUS_CODES = [200, 201]     # IP检测时返回码

POOL_UPPER_THRESHOLD = 200000       # 代理池数量界限


TESTER_CYCLE = 10                   # 代理每次检查周期（秒）
GETTER_CYCLE = 300                  # 代理每次获取周期（秒）


# 测试代理使用的URL，需要检测的加入到列表中
TEST_URL = [ "http://jzsc.mohurd.gov.cn/assets/core/img/common/shpj-close.png", "https://www.baidu.com/img/baidu_resultlogo@2.png" ]

# 配置API服务
API_HOST = '127.0.0.1'              # 代理池API的IP
API_PORT = 55555                    # 代理池API的端口
# 上面配置启动后，代理池访问地址为 http://127.0.0.1:55555

# 开关
TESTER_ENABLED = True               # 测试器的开关
GETTER_ENABLED = True               # 获取器开关
API_ENABLED = True                  # API接口开关

# 每次代理检测量
BATCH_TEST_SIZE = 150

```

- 启动:

```shell
# 如果你的依赖已经安全完成并且具备运行条件,可以直接在Run下运行main.py
# 到Run目录下:
		python main.py
```



### 简单使用

　　启动过几分钟后就能看到抓取到的代理IP，你可以直接到数据库中查看；

　　也可以通过API访问 http://127.0.0.1:55555 查看。

- API

| api       | method | Description    | arg                             |
| --------- | ------ | -------------- | ------------------------------- |
| /         | GET    | 代理池使用简介 | None                            |
| /delete   | GET    | 删除无用的IP   | [proxies, type, detection, pid] |
| /random   | GET    | 获取所需的代理 | [type, detection, limit]        |
| /messages | GET    | 查看代理数量  | None                            |

- 获取IP

　　如果要在爬虫代码中使用的话， 可以将此API封装成类获取IP列表，例如：

```python
import requests


class ipproxy():
    # 可在messages页面查看具体参数信息
    def __init__(self, type= None, detection=None):
        self.type = type
        self.detection = detection

    def init_data(self, data):
        for key in list(data.keys()):
            if not data.get(key):
                del data[key]
        return data

    # 获取代理，返回list类型
    def get_proxy(self, limit):
        params = {
            'type' : self.type,                # 请求的IP类型     （可选参数，默认为：""）
            'detection' : self.detection,      # 请求的测试网站   （可选参数，默认为：""）
            'limit' : limit                    # 每次获取的IP数   （可选参数，默认为：10）
        }
        response = requests.get('http://127.0.0.1:55555/random',params=self.init_data(params))
        return response.text.split("\r\n")

    # 删除代理
    def delete_proxy(self, porxy):
        params = {
            'proxy': porxy,                    # 需要删除的IP     （必填参数）
            'type': self.type,                 # 请求的IP类型     （可选参数，默认为：""）
            'detection': self.detection,       # 请求的测试网站   （可选参数，默认为：""）
            'pid' : 1
        }
        return requests.get('http://127.0.0.1:55555/delete', params=self.init_data(params))

ip = ipproxy(type="https", detection="baidu")
print(ip.get_proxy(3))
"""	['120.79.147.254:9000', '183.146.213.157:80', '192.144.191.242:80'] """


```

### 扩展代理

　　项目默认包含几个免费的代理获取方法，但是免费的毕竟质量不好，所以如果直接运行可能拿到的代理质量不理想。所以，提供了代理获取的扩展方法。

　　添加一个新的代理获取方法如下:

- 1、首先在[Crawler](https://github.com/CRDarwin/Free_ProxyPool/blob/master/proxypool/crawler.py#L23)类中添加你的获取代理的方法(已  `crawl_`  开头)，
  该方法需要以生成器(yield)形式返回 `host:ip` 格式的代理，例如:

```python
def crawl_ip3366(self):
    try:
        ip_url = "http://ged.ip3366.net/api/?key=**&getnum=**&proxytype=**"
        html = get_page(ip_url)
        if html:
            ip_list = html.rstrip("\r\n").split("\r\n")
            for i in ip_list:
                yield i	     # 确保每个proxy都是 host:ip正确的格式就行
        else:
            print("\033[1;31;40m IP3366网站  ---->  爬取网站为空已准备跳过！ \033[0m")
            return 0
    except:
        print("\033[1;41;97m IP3366网站  ---->  爬虫网站规则更改，请修改！ \033[0m")
        return 0
)
```



### 代理采集

   目前实现的采集免费代理网站有(排名不分先后, 下面仅是对其发布的免费代理情况, 付费代理测评可以参考[这里](https://zhuanlan.zhihu.com/p/33576641)): 

| 厂商名称     | 状态           | 更新速度   | 可用率 | 是否被墙 | 地址                                                         |
| ------------ | -------------- | ---------- | ------ | -------- | ------------------------------------------------------------ |
| 无忧代理     | 可用           | 几分钟一次 | *      | 否       | [地址](http://www.data5u.com/free/index.html)                |
| 66代理       | 可用           | 更新很慢   | *      | 否       | [地址](http://www.66ip.cn/)                                  |
| 西刺代理     | 可用           | 几分钟一次 | *      | 否       | [地址](http://www.xicidaili.com)                             |
| 全网代理     | 可用           | 几分钟一次 | *      | 否       | [地址](http://www.goubanjia.com/)                            |
| 训代理       | 已关闭免费代理 | *          | *      | 否       | [地址](http://www.xdaili.cn/)                                |
| 快代理       | 可用           | 几分钟一次 | *      | 否       | [地址](https://www.kuaidaili.com/)                           |
| 云代理       | 可用           | 几分钟一次 | *      | 否       | [地址](http://www.ip3366.net/)                               |
| IP海         | 可用           | 几小时一次 | *      | 否       | [地址](http://www.iphai.com/)                                |
| 免费IP代理库 | 可用           | 快         | *      | 否       | [地址](http://ip.jiangxianli.com/)                           |
| 中国IP地址   | 可用           | 几分钟一次 | *      | 是       | [地址](http://cn-proxy.com/)                                 |
| Proxy List   | 可用           | 几分钟一次 | *      | 是       | [地址](https://proxy-list.org/chinese/index.php)             |
| ProxyList+   | 可用           | 几分钟一次 | *      | 是       | [地址](https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1) |

  如果还有其他好的免费代理网站, 可以在提交在[issues](https://github.com/CRDarwin/Free_ProxyPool/issues), 下次更新时会考虑在项目中支持。

### 问题反馈

　　任何问题欢迎在[Issues](https://github.com/CRDarwin/Free_ProxyPool/issues) 中反馈，如果没有账号可以去 我的微信 (`JJ77128`) 中留言。

　　你的反馈会让此项目变得更加完美。

### 贡献代码

　　本项目仅作为基本的通用的代理池架构，不接收特有功能(当然,不限于特别好的idea)。

　　本项目依然不够完善，如果发现bug或有新的功能添加，请在[Issues](https://github.com/CRDarwin/Free_ProxyPool/issues)中提交bug(或新功能)描述，在确认后提交你的代码。

### Release Notes

   [release notes](#)
   
## 代码的检测部分还没有开发完成！！！

