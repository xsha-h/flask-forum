from functools import wraps

from flask import g, redirect, url_for


def permission_required(permission):
    """
    验证用户的权限，根据权限显示后台的导航栏。如果没有权限，就显示后台的首页
    :param permission: 用户的权限
    :return: 显示后台的导航栏
    """
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outer
