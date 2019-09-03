# MongoDB数据库配置信息
MONGO_HOST = 'localhost'            # MongoDB数据库地址
MONGO_PORT = 27017                  # MongoDB端口
MONGO_PASSWORD = None               # MongoDB密码，如无填None
MONGO_DB = 'tests'                  # MongoDB数据库名称
MONGO_TABLE = 'test_ones'            # MongoDB数据集合

# 代理中pid的类型
DTC_PID = 1                         # 可用IP
DOT_PID = 0                         # 未检测IP

# 代理分数
MAX_SCORE = 160                     # 可用代理分数
MIN_SCORE = 60                      # 移除代理分数
INITIAL_SCORE = 100                 # 进库代理分数
REMOVE_SCORE = 3                    # 可用代理被验证不可用次数,下一次直接删除


VALID_STATUS_CODES = [200, 201]     # IP检测时返回码

POOL_UPPER_THRESHOLD = 200000       # 代理池数量界限


TESTER_CYCLE = 30                   # 代理每次检查周期（秒）
GETTER_CYCLE = 30                   # 代理每次获取周期（秒）


# 测试代理使用的URL，需要检测的加入到列表中
TEST_URL = [ "http://guozhivip.com/rank/","https://www.baidu.com/"]

# API配置
API_HOST = '127.0.0.1'              # 代理池API的IP
API_PORT = 55555                    # 代理池API的端口

# 开关
TESTER_ENABLED = True               # 测试器的开关
GETTER_ENABLED = True               # 获取器开关
API_ENABLED = True                  # API接口开关

# 每次代理检测量
BATCH_TEST_SIZE = 150
