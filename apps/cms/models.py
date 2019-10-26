from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class CMSPermission(object):
    """
    通过二进制的方式赋予7种权限，二进制的方式能更好的显示用户的叠加权限
    之后可以通过 &（与运算） 判断用户的权限、通过 |（或运算）赋予用户的权限
    """
    # 255的二进制方式来表示11111111
    # 1、超级管理员权限
    ALL_PERMISSION = 0b11111111
    # 2、访问者权限
    VISITOR =        0b00000001
    # 3、管理帖子权限
    POSTER =         0b00000010
    # 4、管理评论权限
    COMMENTER =      0b00000100
    # 5、管理板块权限
    BOARDER =        0b00001000
    # 6、管理前台用户权限
    FRONTUSER =      0b00010000
    # 7、管理后台用户权限
    CMSUSER =        0b00100000
    # 8、后台管理员权限
    ADMINER =        0b01000000


# 用户和角色多对多的桥接表
cms_role_user = db.Table(
    "cms_role_user",
    db.Column("cms_role_id", db.Integer, db.ForeignKey("cms_role.id"), primary_key=True),
    db.Column("cms_user_id", db.Integer, db.ForeignKey("cms_user.id"), primary_key=True),
)


class CMSRole(db.Model):
    __tablename__ = "cms_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)
    users = db.relationship("CMSUser", secondary=cms_role_user, backref="roles")


class CMSUser(db.Model, UserMixin):
    """
    定义一个类名，系统将类转换为表格，表名为cms_user
    定义类的属性就是表格的字段名
    为了安全性，可以将用户表的password属性置为保护属性如    _password
    为了方便用户操作保护属性像操作普通属性一样，需要装饰 _password
    在设置密码的过程中，需要对密码加密——>调用generate_password_hash()
    另外定义一个校验密码的方法check_password()
    在校验密码的过程中，需要对密码解密——>调用check_password_hash()
    """
    __tablename__ = "cms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        """
        获取用户的密码（也是加密后的密码）
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw_password):
        """
        设置密码
        :param raw_password: 前端后台传入的密码参数
        :return:没有返回值
        """
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """
        校验密码，将数据库的存入的密码解密之后再与传入的密码参数匹配
        :param raw_password: 前端后台传入的密码参数
        :return: True or False
        """
        result = check_password_hash(self.password, raw_password)
        return result

    """
    在前台用户类定义权限是因为用户和角色是多对多的关系。
    前台用户可以拥有多个角色，每个角色对以一个权限
    所以可以通过操控属性permission获取或者检验用户的权限
    """
    @property
    def permission(self):
        """
        获取用户下的所有权限
        :return: 所有权限
        """
        if not self.roles:
            return 0
        all_permission = 0
        for role in self.roles:
            permissions = role.permissions
            all_permission |= permissions
        return all_permission

    def has_permission(self, permission):
        """
        检验用户是否含有某种权限
        :param permission: 权限参数
        :return: True or False
        """
        return self.permission&permission == permission

    @property
    def is_developer(self):
        """
        检验用户是否是开发者（超级管理员）
        :return: True or False
        """
        return self.has_permission(CMSPermission.ALL_PERMISSION)
