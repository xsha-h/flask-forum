# 钩子函数
from flask import session, g

from apps.cms import bp
from .models import CMSUser, CMSPermission


@bp.before_request
def before_request():
    """
    检验session中存取的用户相关信息是否可以通过 “user_id”获取当前登录的用户
    :return:
    """
    if "user_id" in session:
        g.cms_user = CMSUser.query.get(session["user_id"])


@bp.context_processor
def cms_context_processor():
    """
    定义模板的全局变量
    主要作用是将python类的相关属性能用在模板上，
    让模板想使用类一样访问属性
    :return:
    """
    return {"CMSPermission": CMSPermission}
