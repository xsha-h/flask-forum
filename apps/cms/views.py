import random
import string
import os

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g
from flask_login import login_required, LoginManager,current_user
from flask_login import login_user, logout_user
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import secure_filename

from apps.cms.decorators import permission_required
from apps.models import BannerModel, BoardModel, PostModel, HighlightPostModel, CommentModel
from exts import db, mail
from flask_mail import Message
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, \
    UpdateBoardForm
from .models import CMSUser, CMSPermission
from utils import restful, cpcache

# 指定没有登录时重定向的页面,需要将LoginManager的实例化对象初始化app(在入口文件中)
# login_manager = LoginManager()
from apps.front import login_manager
# login_manager.blueprint_login_views = "cms.login"
# 定义蓝图对象
bp = Blueprint("cms", __name__)


UPLOAD_PATH = os.path.join("static/front/images/index_images")


@bp.route("/", methods=["GET"])
@login_required
def index():
    g.cms_user = current_user

    return render_template("cms/cms_index.html")


class LoginView(views.MethodView):
    """
    get方法对应前端后台的get请求，主要是渲染页面
    post方法对应前端后台的post请求：
        1、先验证用户的输入是否符合表单验证的要求，如果不符合要求，则返回具体的错误
        2、先通过邮箱查找用户并通过查找的用户密码与后台表格密码进行验证，如果没有找到，返回邮箱或者密码错误
        3、匹配成功则通过login_user(user)自动保存session值,前端页面通过当前登录用户的代理current_user使用相关属性，
            并且将用户保存g对象中供后期代码使用
        4、通过获取前端后台的remember值给session定义过期时间，默认是浏览器会话关闭
    """
    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter(CMSUser.email == email).first()
            if user and user.check_password(password):
                # 自动生成一个session值
                login_user(user)
                session['type'] = 'cms'
                # 将登录用户保存到g对象中
                g.cms_user = user
                if remember:
                    # 设置session的过期时间，默认为31天
                    session.permanent = True
                    return redirect(url_for("cms.index"))
                return redirect(url_for("cms.index"))
            else:
                return self.get(message="邮箱或者密码错误")
        else:
            message = form.get_error()
            return self.get(message=message)


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))


@bp.route("/logout")
@login_required
def logout():
    """
    后台管理系统注销并将所有的cookies删除
    :return:
    """
    logout_user()
    return redirect(url_for("cms.login"))


# @login_manager.user_loader
# def load_user(user_id):
#     """
#     后台用户类必须继承UserMixin,以防用户表没有定义校验的字段，如：is_active等
#     :param user_id:
#     :return:
#     """
#     session['type'] = 'hou'
#     return CMSUser.query.get(user_id)


@bp.route("/profile")
@login_required
def profile():
    """
    个人信息页面展示
    :return:
    """
    return render_template("cms/cms_profile.html")


class ResetPwdView(views.MethodView):
    """
    get方法对应前端后台的get请求，主要是渲染页面
    post方法对应前端后台的post请求：
        1、先验证用户的输入是否符合表单验证的要求，如果不符合要求，则返回具体的错误
        2、先通过前端传入的旧密码与当前登录的用户的密码就行验证（g.cms_user）
        3、匹配成功则将新密码赋值给当前用户，保存即可
        4、以上三步是忽略csrf攻击时的工作
        5、为保证页面局部刷新，前端需要使用Ajax请求，ajax请求防止csrf的方式：
            1）在页面上定义一个name为csrf-token的meta标签
            2）重写Ajax请求返回一个X-CSRFtoken响应
        6、为适应前端json数据格式，需要同意创建一个包，专门处理前端请求返回的状态码及信息（utils/restful.py)
    """
    @login_required
    def get(self):
        return render_template("cms/cms_resetpwd.html")
    
    @login_required
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return {"code": 200, "message": ""}
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule("/resetpwd", view_func=ResetPwdView.as_view("resetpwd"))


@bp.route("/email_captcha")
def email_captcha():
    """
    发送邮件我们不需要跳转页面，不需要重定向；邮件地址信息只需通过get方式请求即可
    后台获取邮件信息需要进行相关的判断，没有通过验证就将信息（状态码，信息）发送到前端页面（js文件处理）
    通过验证，我们需要自制验证码，将验证码发送到接收者邮件，并且以邮件地址为键，验证码为值保存到redis缓存中
    :return:
    """
    # /email_captcha/?email=XXX@qq.com
    email = request.args.get("email")
    if not email:
        return restful.params_error("请输入邮箱地址")

    # 获取所有的字母（大小写）并且转换成列表
    source = list(string.ascii_letters)
    # 再次获取数字,并且拼接到source中
    source.extend(map(lambda x: str(x), range(0, 10)))

    # 从source中随机取样返回的是一个列表，通过join方式将其变成字符串作为验证码
    captcha = "".join(random.sample(source, 6))
    # 定义一个信息类实例，传递邮件标题，邮件接收者，邮件内容
    message = Message("校园论坛邮箱验证码", recipients=[email], body="您的验证码是：%s" % captcha)
    try:
        # 通过邮件类实例发送上面封装的信息类实例
        mail.send(message)
    except:
        return restful.server_error()

    # 将邮件保存到redis数据库中（修改邮箱通过在redis缓存中取出验证码）
    cpcache.set(email, captcha)

    return restful.success()


class ResetEmailView(views.MethodView):
    """
    get方法对应前端后台的get请求，主要是渲染页面
    post方法对应前端后台的post请求：
        1、获取前台传来的验证码，通过表单验证与在redis缓存的验证码进行匹配
        2、匹配成功则将新邮箱赋值给当前用户，保存即可
        4、以上三步是忽略csrf攻击时的工作
        5、为保证页面局部刷新，前端需要使用Ajax请求，ajax请求防止csrf的方式：
            1）在页面上定义一个name为csrf-token的meta标签
            2）重写Ajax请求返回一个X-CSRFtoken响应
        6、为适应前端json数据格式，需要同意创建一个包，专门处理前端请求返回的状态码及信息（utils/restful.py)
    """
    @login_required
    def get(self):
        return render_template("cms/cms_resetemail.html")

    @login_required
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule("/resetemail", view_func=ResetEmailView.as_view("resetemail"))


@bp.route("/banners")
def banners():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    PER_PAGE = 10
    # 分页实现
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    banners = BannerModel.query.slice(start, end)
    total = BannerModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    context = {
        "pagination": pagination,
        "banners": banners,
    }
    return render_template("cms/cms_banners.html", **context)


# def uptoken(filename):
#     filename = search(filename)
#     # 填写相关AK和SK
#     access_key = "4a4DisPJLcpZ50Vi285MNLUtOMP3GfpioiyI2COK"
#     secret_key = "DS_4Tg6DcKF8qrkOojJmik2q2EcvI24SAI7rZU1K"
#     # 构建鉴权对象
#     q = qiniu.Auth(access_key, secret_key)
#
#     # 要上传的空间
#     buckek_name = "campus"
#     # 上传后保存的文件名
#     key = filename
#     # 生成上传token，可以指定过期时间
#     token = q.upload_token(buckek_name, key, 3600)
#
#     print(token)
#     # 上传文件的绝对路径
#     localfile = filename
#     ret, info = qiniu.put_file(token, key, localfile)
#     print(info)
#     return None


@bp.route("/uploadfile", methods=["POST"])
def uploadfile():
    # 获取文件信息
    file_info = request.files.get("image")
    if file_info:
        # 组织成一个标准的文件路径，如果标准文件为空，就不保存文件
        format_file = secure_filename(file_info.filename)
        # 上传文件
        file_info.save(os.path.join(UPLOAD_PATH, format_file))
        return restful.success()
    return restful.params_error(message="图片保存失败！")


@bp.route("/abanner", methods=["POST"])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        print(form.errors)
        return restful.params_error(message=form.get_error())


@bp.route("/ubanner", methods=["POST"])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        bannerId = form.bannerId.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(bannerId)

        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority

            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个轮播图")
    else:
        print(form.errors)
        return restful.params_error(form.get_error())


@bp.route("/dbanner", methods=["POST"])
def dbanner():
    bannerId = request.form.get("bannerId")
    if not bannerId:
        return restful.params_error(message="请输入轮播图的id")

    banner = BannerModel.query.get(bannerId)
    if not banner:
        return restful.params_error(message="没有这个轮播图")

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


# 下面6个视图函数都是需要进行权限验证才能展示导航栏
@bp.route("/posts")
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    PER_PAGE = 10
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    post_list = PostModel.query.slice(start, end)
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    context = {
        "posts": post_list,
        "pagination": pagination,
    }
    return render_template("cms/cms_posts.html", **context)


@bp.route("/hpost", methods=["POST"])
@permission_required(CMSPermission.POSTER)
def hpost():
    postId = request.form.get("postId")
    if not postId:
        return restful.params_error(message="请传入帖子id！")

    post = PostModel.query.get(postId)
    if not post:
        return restful.params_error(message="没有这篇帖子！")
    highlight = HighlightPostModel(post=post)
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route("/uhpost", methods=["POST"])
@permission_required(CMSPermission.POSTER)
def upost():
    postId = request.form.get("postId")
    if not postId:
        return restful.params_error(message="请传入帖子id！")

    post = PostModel.query.get(postId)
    if not post:
        return restful.params_error(message="没有这篇帖子！")
    highlight = HighlightPostModel.query.filter_by(post_id=postId).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route("/comments")
@permission_required(CMSPermission.COMMENTER)
def comments():
    context = {
        "comments": CommentModel.query.all()
    }
    return render_template("cms/cms_comments.html", **context)


@bp.route("/boards")
@permission_required(CMSPermission.BOARDER)
def boards():
    boards_model = BoardModel.query.all()
    return render_template("cms/cms_boards.html", boards=boards_model)


@bp.route("/aboard", methods=["POST"])
@login_required
def aboard():
    form = AddBoardForm(request.form)
    print(request.form.get("name"))
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/uboard", methods=["POST"])
@login_required
def uboard():
    form = UpdateBoardForm(request.form)
    print(request.form.get("boradId"))
    if form.validate():
        boardId = form.boardId.data
        name= form.name.data
        board = BoardModel.query.get(boardId)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块")
    else:
        return restful.params_error(form.get_error())


@bp.route("/dboard", methods=["POST"])
@login_required
def dboard():
    boardId = request.form.get("boardId")
    if not boardId:
        return restful.params_error(message="请传入板块的id")

    board = BoardModel.query.get(boardId)
    if not board:
        return restful.params_error(message="没有这个板块")

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route("/fusers")
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")


@bp.route("/cusers")
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")


@bp.route("/croles")
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template("cms/cms_croles.html")
