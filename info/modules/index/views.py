from . import index_blu
from flask import render_template,current_app
from flask import session
from info.models import User
from info.models import News
from info import constants


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
    # 获取点击排行数据
    news = None

    try:
        news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_list = []
    if news:
        for new in news:
            news_list.append(new.to_basic_dict())
    data = {
        "user_info": user.to_dict() if user else None,
        "news_list": news_list
    }

    return render_template("news/index.html", data=data)


@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")

