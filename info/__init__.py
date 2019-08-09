from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect

# session拓展工具将flask中的session存储到redis
from flask_session import Session
from config import config_dict
import pymysql

# python2和python3数据库相互转化使用
pymysql.install_as_MySQLdb()

# 当app不存在的时候，只是进行申明，并没有真实创建数据库对象db
db = SQLAlchemy()

# 全局变量，申明未空类型数据
redis_store = None  # type:StrictRedis


# 工厂方法
# development ---> DevelopmentConfig
# production  ---> ProductionConfig

def create_app(config_name):
    # 1.创建app对象
    app = Flask(__name__)

    # 2.将配置信息添加到app上
    config_class = config_dict[config_name]  # DevelopmentConfig

    # DevelopmentConfig ---赋予app属性为：开发模式app
    # ProductionConfig --- 赋予app属性为：线上模式app
    app.config.from_object(config_class)

    # 3.数据库对象（mysql&redis）
    # mysql数据库对象
    # 延迟加载，懒加载，当app有值的时候我才真正进行数据库初始化工作
    db.init_app(app)

    # redis数据库对象
    global redis_store
    redis_store = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)

    # 4.给项目添加csrf保护机制
    # 1.提取cookie中的csrf_token
    # 2.如果数据是通过表单发送：提取表单中的csrf_token， 如果数据是通过ajax请求发送：提取请求头中的字段X-CSRFToken
    # 3.对比这两个值是否一致
    CSRFProtect(app)

    # 5.创建Flask_session工具类对象：将flask.session的存储从 服务器`内存` 调整到 `redis`数据库
    Session(app)

    # 返回app对象
    return app
