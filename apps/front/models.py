from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
import shortuuid


class GenderEnum(Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOWN = 4


class FrontUser(db.Model, UserMixin):
    """
    定义一个类名，系统将类转换为表格，表名为front_user
    定义类的属性就是表格的字段名
    为了安全性，可以将用户表的password属性置为保护属性如    _password
    为了方便用户操作保护属性像操作普通属性一样，需要装饰 _password
    在设置密码的过程中，需要对密码加密——>调用generate_password_hash()
    另外定义一个校验密码的方法check_password()
    在校验密码的过程中，需要对密码解密——>调用check_password_hash()
    """
    __tablename__ = "front_user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOWN)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get("password")
            kwargs.pop("password")
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)
