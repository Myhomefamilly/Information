from redis import StrictRedis
import logging


# 创建项目配置类
class Config(object):
    """自定义项目父类"""

    # mysql数据配置
    # 连接mysql数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information"
    # 开启数据库跟踪修改操作
    SQLALCHEMY_TRACK_MODIFICATICATIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库的配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 使用session需要设置加密字符串
    SECRET_KEY = "wewewefdvfsd4"
    # SESSION_TYPE = 'filesystem'


    # 将flask.session的存储从服务器'内存'调整到'redis'数据库配置如下
    SESSION_TYPE = 'reids'  # 标明存储的数据类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)  # redis对象
    SESSION_USE_SIGNER = True  # 对于session_id需要进行加密处理
    SESSION_PERMANENT = False  # redis中的session数据不需要永久处理
    PERMANENT_SESSION_LIFETIME = 86400  # 设置redis中session过期时常


class DevelopmentConfig(Config):
    """开发模式的项目配置信息"""
    # 开启项目调试模式
    DEBUG = True
    # 开发模式的日志设置为：DEBUG
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """线上模式的项目配置信息"""
    # 线上模式不需要debug信息查看　减少IO压力
    DEBUG = False
    # 线上模式的日志设置: ERROR
    LOG_LEVEL = logging.ERROR


# 提供一个接口供外界调用
# 使用方式：config_dict["development"] --> DevelopmentConfig
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
