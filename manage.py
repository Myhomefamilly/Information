from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# 我们存储数据用到的session
from flask import session
from info import create_app, db

"""
manage.py文件只需要负责项目启动＆数据库的迁移即可，
其他配置信息，app相关信息都应该抽取到特定文件中
"""

# 传入的参数是development获取开发模式对应的app对象
# 传入的参数是production获取线上模式对应的app对象
app = create_app("development")

# 6.创建管理对象
manager = Manager(app)

# 7.创建迁移对象
Migrate(app, db)

# 8.添加迁移命令
manager.add_command('db', MigrateCommand)


def hello_world():
    session["name"] = "laowang"
    return "hello world!"


if __name__ == '__main__':
    # app.run()
    # 9.使用管理对象运行项目
    manager.run()
