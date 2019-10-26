from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    """
    父类表单主要是输出表单验证不成功的第一条错误信息
    """
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super().validate()
