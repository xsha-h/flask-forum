from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from apps.front.models import FrontUser
from apps.models import BannerModel, BoardModel, PostModel
from exts import db
from apps.cms import models as cms_models

# 获取模型中定义的类
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

app = create_app()
# 定义Manager类实例化对象
manage = Manager(app)

# 将app应用与db数据库绑定到迁移文件中
Migrate(app, db)
# 将迁移文件用到的命令换成db开头（manage.py文件可以自定义命令）添加到manage中
manage.add_command("db", MigrateCommand)


@manage.option("-u", "--username", dest="username")
@manage.option("-p", "--password", dest="password")
@manage.option("-e", "--email", dest="email")
def create_cms_user(username, password, email):
    """
    自定义创建后台用户的命令，在cmd命令行中输入类似于如下命令，即可添加用户：（在虚拟环境下）
        python manage.py db create_cms_user -u 用户名 -p 密码 -e 邮箱地址
    :param username:
    :param password:
    :param email:
    :return: 返回一提示消息
    """
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


@manage.command
def create_role():
    # 1、访问者权限（修改个人信息）
    visitor = CMSRole(name="访问者", desc="只能查看数据，不能修改")
    visitor.permissions = CMSPermission.VISITOR
    # 2、运营角色（修改个人信息，管理帖子、评论、前台用户
    operator = CMSRole(name="运营", desc="管理帖子、评论、前台用户")
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | \
                           CMSPermission.FRONTUSER | CMSPermission.CMSUSER
    # 3、管理员（拥有绝大部分权限）
    admin = CMSRole(name="管理员", desc="拥有本系统所有权限")
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | \
                           CMSPermission.FRONTUSER | CMSPermission.CMSUSER | CMSPermission.BOARDER
    # 4、开发者
    developer = CMSRole(name="开发者", desc="开发人员专用角色")
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manage.option("-e", "--email", dest="email")
@manage.option("-n", "--name", dest="name")
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功！")
        else:
            print("没有这个角色：%s！" % role)
    else:
        print("%s邮箱没有这个用户！" % email)


@manage.command
def test_permission():
    user = CMSUser.query.filter_by(id=2).first()
    if user.has_permission(CMSPermission.VISITOR):
        print("这个用户拥有访问者权限")
    else:
        print("这个用户没有访问者权限")


@manage.option("-t", "--telephone", dest="telephone")
@manage.option("-p", "--password", dest="password")
@manage.option("-u", "--username", dest="username")
def create_front_user(telephone, password, username):
    user = FrontUser(telephone=telephone, password=password, username=username)
    db.session.add(user)
    db.session.commit()


@manage.command
def create_test_post():
    for i in range(351, 401):
        title = "帖子标题:{}".format(i)
        content = "帖子内容:{}".format(i)
        author = FrontUser.query.first()
        board = BoardModel.query.all()[9]
        post = PostModel(title=title, content=content)
        post.author = author
        post.board = board
        db.session.add(post)
        db.session.commit()
    print("所有帖子添加成功！")


if __name__ == "__main__":
    manage.run()
