from wtforms import StringField, IntegerField
from wtforms.validators import Regexp, EqualTo, ValidationError, DataRequired

from apps.forms import BaseForm
from utils import cpcache


class SignupForm(BaseForm):
    """
    注册信息表单验证主要是验证两个验证码：短信验证码和图形验证码
    两者的验证码验证方式是一样的，它们分别通过手机号、图形验证码文本值获取对应的验证码
    """
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}", message="请输入正确的短信验证码")])
    username = StringField(validators=[Regexp(r".{2, 20}", message="请输入正确格式的用户名")])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z._]{6, 20}", message="请输入正确格式的密码")])
    password2 = StringField(validators=[EqualTo("password1", message="两次密码输入不正确")])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message="请输入正确的图形验证码")])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = cpcache.get(telephone)
        if not sms_captcha_mem or sms_captcha.lower() != sms_captcha_mem.lower():
            raise ValidationError("短信验证码错误")

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        graph_captcha_mem = cpcache.get(graph_captcha.lower())
        if not graph_captcha_mem or graph_captcha.lower() != graph_captcha_mem.lower():
            raise ValidationError("图形验证码错误")


class SigninForm(BaseForm):
    """
    登录信息表单验证主要是验证图形验证码
    在缓存中通过图形验证码文本值获取对应的验证码
    """
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
    password = StringField(validators=[Regexp(r"[0-9A-Za-z._]", message="请输入正确格式的密码")])
    remember = StringField()
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message="请输入正确的图形验证码")])

    def validate_graph_captcha(self, field):
        graph_captcha = field.data.replace("", " ")[1:-1]
        graph_captcha_mem = cpcache.get(graph_captcha.lower())
        print("验证码：", graph_captcha, graph_captcha_mem)
        if not graph_captcha_mem or graph_captcha.lower() != graph_captcha_mem.lower():
            raise ValidationError("图形验证码错误")


class AddPostForm(BaseForm):
    title = StringField(validators=[DataRequired(message="请输入标题！")])
    content = StringField(validators=[DataRequired(message="请输入内容！")])
    boardId = IntegerField(validators=[DataRequired(message="请输入板块id！")])


class AddCommentForm(BaseForm):
    content = StringField(validators=[DataRequired(message="请输入评论内容！")])
    postId = IntegerField(validators=[DataRequired(message="请输入帖子id！")])
