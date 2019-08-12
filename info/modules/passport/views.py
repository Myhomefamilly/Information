from . import passport_blu
from flask import request, current_app, jsonify
from flask import make_response

from info import redis_store
from info import constants
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from info.lib.yuntongxun.sms import CCP
from info.models import User
import re
import random


@passport_blu.route("/image_code")
def get_image_code():
    """
    获取图片验证码
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


@passport_blu.route("/smscode", methods=["get", "post"])
def send_sms():
    """
    获取短信验证码
    """
    # 接受请求参数
    mobile = request.json.get("mobile")
    image_code = request.json.get("image_code")
    image_code_id = request.json.get("image_code_id")
    # 校验
    if all([mobile, image_code, image_code_id]) is False:
        return jsonify(error=RET.PARAMERR, errmsg="缺少必传参数")

    if not re.match(r"^1[3-9]\d{9}$", mobile):
        return jsonify(error=RET.DATAERR, errmsg="手机号格式不对")

    server_image_code = redis_store.get("ImageCode_%s" % image_code_id)

    if not server_image_code:
        return jsonify(error=RET.NODATA, errmsg="图片验证码过期")

    redis_store.delete("ImageCode_%s" % image_code_id)

    if image_code.lower() != server_image_code.lower():
        return jsonify(error=RET.DATAERR, errmsg="图形验证码错误")

    # 判断手机号是否重复
    try:
        user = User.query.filter_by(mobile=mobile).first()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="数据库查询错误")
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg="该手机已被注册")

    # 业务逻辑
    # 随机生成短信码
    sms_code = "%06d" % random.randint(0, 999999)
    print(sms_code)
    # 保存短信验证码
    redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
    # 发送短信
    # result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], "1")

    # if result != 0:
    #     return jsonify(error=RET.THIRDERR, errmsg="发送短信失败")

    # 返回数据
    return jsonify(error=RET.OK, errmsg="发送短信成功")
