from flask import g
from flask_wtf.file import FileAllowed

from utils import cpcache
from ..forms import BaseForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(BaseForm):
    email = StringField(validators=[DataRequired(message="请输入邮箱地址"), Email(message="请输入正确的邮箱格式")])
    password = StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd")])

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱地址")])
    captcha = StringField(validators=[Length(6, 6, message="请输入正确长度的验证码")])

    def validate_captcha(self, field):
        """
        表单验证过程，从redis缓存中获取邮件对应的验证码与前台传来的验证码匹配
        :param field:
        :return:
        """
        captcha = field.data
        email = self.email.data
        captcha_cache = cpcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if email == user.email:
            raise ValidationError("不能修改为相同的邮箱！")


class AddBannerForm(BaseForm):
    name = StringField(validators=[DataRequired(message="请输入轮播图名称！")])
    image_url = StringField(validators=[DataRequired(message="请输入图片链接！")])
    link_url = StringField(validators=[DataRequired(message="请输入跳转链接！")])
    priority = IntegerField(validators=[DataRequired(message="请输入轮播图优先级！")])


class UpdateBannerForm(AddBannerForm):
    bannerId = IntegerField(validators=[DataRequired(message="请输入轮播图的id！")])


class AddBoardForm(BaseForm):
    name = StringField(validators=[DataRequired(message="请输入板块名称！")])


class UpdateBoardForm(AddBoardForm):
    boardId = IntegerField(validators=[DataRequired(message="请输入板块的id！")])
