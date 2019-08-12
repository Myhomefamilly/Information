from . import index_blu
from flask import render_template,current_app
from flask import session
from info.models import User


@index_blu.route("/")
def index():
    # 获取当前登录id
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    return render_template("news/index.html", data={"user_info": user.to_dict() if user else None})


@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")

