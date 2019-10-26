from wtforms import StringField
from wtforms.validators import regexp, DataRequired

from apps.forms import BaseForm
import hashlib


class SMSCaptchaForm(BaseForm):
    """
    手机短信验证码的封装，防止黑客或者高手仿照地址栏上的url发送短信
    通过一些干扰信息将手机号和验证码更好的封装，
    后台和前台要商量好加密机制，双方经过同样的加密机制，得到相同的字符串才能发送短信
    比如使用md5加密让手机号码和时间戳和盐变量组合在一起，返回一个加了密的字符串
    """
    salt = "347tgfreuydx9384t5rei3458923"
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}")])
    timestamp = StringField(validators=[regexp(r"\d{13}")])
    sign = StringField(validators=[DataRequired()])

    def validate(self):
        result = super().validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(telephone+timestamp+sign)
        # md5函数必须传递一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode("utf-8")).hexdigest()
        if sign2 == sign:
            return True
        else:
            return False
