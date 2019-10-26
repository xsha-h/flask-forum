from io import BytesIO

from flask import Blueprint, request, make_response

from apps.common.forms import SMSCaptchaForm
from utils import restful, cpcache
from utils.alidayu import Alidayu
from utils.captcha import Captcha


bp = Blueprint("common", __name__)


@bp.route("/")
def index():
    return "common index"


# @bp.route("/sms_captcha")
# def sms_captcha():
#     telephone = request.args.get("telephone")
#     if not telephone:
#         return restful.params_error(message="请输入手机号码")
#
#     # 借用图形验证码类中的获取随机验证码的方法
#     captcha = Captcha.gene_text(numbers=4).replace(" ", "")
#     # 你把telephone换成具体的手机号码，captcha换成具体的验证码值
#     alidayu = Alidayu()
#     if alidayu.send_sms(telephone, captcha):
#         return restful.success()
#     else:
#         return restful.params_error(message="验证码发送失败！")


@bp.route("/captcha")
def graph_captcha():
    """
    使用定义好的图形验证码类，来制作验证码
    以验证码为键、验证码为值（为了用户的体验，让其忽略大小写）存储在redis缓存中
    通过BytesIO字节流的方式保存和访问图片
    :return: 图片响应
    """
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    cpcache.set(text.lower(), text.lower())
    print("图形验证码：", cpcache.get(text.lower()))
    # BytesIO:字节流
    out = BytesIO()
    # 保存图片
    image.save(out, "png")
    # 存储完图片，将文件的指针指向文件头，使下次保存图片能覆盖前面保存的图片，节省空间
    out.seek(0)
    # 访问图片，并将其作为一个响应返回给前台
    resp = make_response(out.read())
    resp.content_type = "image/png"
    return resp


@bp.route("/sms_captcha", methods=["POST"])
def sms_captcha():
    """
    前台将手机号和时间戳和盐封装成一个字符串传给表单验证，通过验证才能发送验证码
    以手机号为键、短信验证码为值保存到redis缓存中
    :return:
    """
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        # 制作验证码时中间有空格字符串，需要使用空字符串代替空格字符串
        captcha = Captcha.gene_text(numbers=4).replace(" ", "")
        # 定义阿里类实例，使用api即可
        alidayu = Alidayu()
        if alidayu.send_sms(telephone, captcha):
            # 将相关的信息保存的redis缓存中
            cpcache.set(telephone, captcha, 60)
            return restful.success()
        else:
            return restful.params_error(message="参数错误！")
    return restful.params_error(message="参数错误！")



