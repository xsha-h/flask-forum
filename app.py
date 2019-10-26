from flask import Flask
from flask_wtf import CSRFProtect
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
# from apps.cms import login_manager as cms_login_manager
from apps.front import login_manager as front_login_manager


import config
from exts import db, mail, cache, ckeditor


def create_app():
    """
    主入口文件创建app，供其他蓝图使用
    :return: 返回一个app
    """
    app = Flask(__name__)
    # 防止csrf注入攻击
    CSRFProtect(app)
    # 注册蓝图模块
    app.register_blueprint(cms_bp, url_prefix="/cms")
    app.register_blueprint(common_bp, url_prefix="/common")
    app.register_blueprint(front_bp)

    # 导入配置文件
    app.config.from_object(config)
    # 数据库db绑定到app上
    db.init_app(app)
    # 邮件mail绑定到app上
    mail.init_app(app)
    # Redis数据库cache绑定到app上
    cache.init_app(app)
    # 后台登录login_manager初始化app
    # cms_login_manager.init_app(app)
    # 前台登录login_manager绑定到app上
    front_login_manager.init_app(app)
    # login_manager.blueprint_login_views = "cms.login"
    # login_manager.blueprint_login_views = "/signin"
    front_login_manager.blueprint_login_views = {
        'cms': "cms.login",
        'front': 'front.signin'
    }

    # 富文本编辑器绑定到app上
    ckeditor.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
