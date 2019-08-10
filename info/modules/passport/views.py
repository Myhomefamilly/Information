from . import passport_blu
from flask import request, current_app, jsonify
from flask import make_response

from info import redis_store
from info import constants
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET


@passport_blu.route("/image_code")
def get_image_code():
    """
    获取短信验证码
    :return: image 图片
    """

    # 1.获取到当前图片编号id
    code_id = request.args.get("code_id")

    # 2.生成验证码
    # name唯一标识，text图片验证字符串，图片验证bytes
    name, text, image = captcha.generate_captcha()

    try:
        # 3.将图形验证码保存到redis数据库
        redis_store.setex("ImageCode_%s" % code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(error=RET.DATAERR, errmsg="保存图片验证码失败"))

    # 4.响应内容image及响应格式
    resp = make_response(image)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp
