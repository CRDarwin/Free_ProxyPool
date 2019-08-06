# Redis数据库地址
MONGO_HOST = 'localhost'
# Redis端口
MONGO_PORT = 27017
# Redis密码，如无填None
MONGO_PASSWORD = None
#redis数据库名称
MONGO_DB = 'test'
MONGO_TABLE = 'test_one'


DTC_PID = 1     #可用IP
DOT_PID = 0     #未检测IP(Did not detect)


# 代理分数
MAX_SCORE = 160     #可用代理分数
MIN_SCORE = 60     #移除代理分数
INITIAL_SCORE = 100     #进库代理分数

VALID_STATUS_CODES = [200, 201]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 200000

# 检查周期
TESTER_CYCLE = 10
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL =["http://jzsc.mohurd.gov.cn/assets/core/img/common/shpj-close.png", "https://www.baidu.com/"]

# API配置
API_HOST = '127.0.0.1'
API_PORT = 55555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 150
