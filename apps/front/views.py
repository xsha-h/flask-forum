import os

from flask import Blueprint, views, render_template, request, session, g, url_for, redirect, current_app, abort
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
from flask_login.config import EXEMPT_METHODS
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func

from apps.cms.models import CMSUser
from apps.front.forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from apps.front.models import FrontUser
from apps.models import BoardModel, BannerModel, PostModel, CommentModel, HighlightPostModel
from exts import db
from utils import restful, safeutils
from functools import wraps


bp = Blueprint("front", __name__)
login_manager = LoginManager()
# login_manager.blueprint_login_views = "/signin"


@bp.app_template_global("username")
def global_username():
    """
    定义模板的全局变量，在模板中使用username()
    :return:
    """
    if "type" not in session.keys():
        session['type'] = None
    if session["type"] == "front":
        username = current_user.username
        print(username)
        return username
    return None


def login_required(func):
    """
    重写登录验证
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        else:
            if current_user.is_authenticated:
                if session['type'] != 'front':
                    return current_app.login_manager.unauthorized()
            # return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


@bp.route("/")
def index():
    # 当前板块
    boardId = request.args.get("bd", type=int, default=None)
    # 当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 获取排序选项
    sort = request.args.get("st", type=int, default=1)

    PER_PAGE = 10
    # 优先级排前5的轮播图
    banners = BannerModel.query.all()[:5]
    # 板块
    boards = BoardModel.query.all()
    # 分页实现
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    # 帖子
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精时间排序，没有则按照普通帖子时间排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if boardId:
        query_obj = query_obj.filter(PostModel.board_id == boardId)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total)

    context = {
        "banners": banners,
        "boards": boards,
        "posts": posts,
        "pagination": pagination,
        "current_board": boardId,
        "current_sort": sort,
    }
    return render_template("front/front_index.html", **context)


# @bp.route("/captcha")
# def graph_captcha():
#     # 获取验证码
#     text, image = Captcha.gene_graph_captcha()
#     # BytesIO:字节流
#     out = BytesIO()
#     image.save(out, "png")
#     out.seek(0)
#     resp = make_response(out.read())
#     resp.content_type = "image/png"
#     return resp


# @bp.route("/sms_captcha")
# def sms_captcha():
#     # params = {'code': 'abcd'}  # abcd就是发送的验证码，code就是模板中定义的变量
#     aliobj = Alidayu()
#     result = aliobj.send_sms("18470154449", "abcd")
#     if result:
#         return '发送成功'
#     else:
#         return '发送失败'


class SignupView(views.MethodView):
    """
    如果直接输入注册的url地址，就不会在注册成功之后跳转到上一次访问的url地址
    """
    def get(self):
        # 上一次访问的url地址
        return_to = request.referrer
        # 上一次访问地址存在、上一次访问地址不是当前url地址、上一次访问地址是安全的（是指同一个域名或者IP地址）
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            # 注册成功之后就跳转到上一次访问的地址
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template("front/front_signup.html")

    def post(self):
        """
        将注册的信息放置在表单验证，经过验证就就保存新用户
        :return:
        """
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(username=username, telephone=telephone, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    """
    get方法对应前端后台的get请求，主要是渲染页面：
        如果直接输入登录的url地址，就不会在登录成功之后跳转到上一次访问的url地址
    post方法对应前端后台的post请求：
        1、先验证用户的输入是否符合表单验证的要求，如果不符合要求，则返回具体的错误
        2、先通过邮箱查找用户并通过查找的用户密码与后台表格密码进行验证，如果没有找到，返回邮箱或者密码错误
        3、匹配成功则通过login_user(user)自动保存session值,前端页面通过当前登录用户的代理current_user使用相关属性，
            并且将用户保存g对象中供后期代码使用
        4、通过获取前端后台的remember值给session定义过期时间，默认是浏览器会话关闭
    """
    def get(self):
        # 上一次访问的url地址
        return_to = request.args.get("return_to")
        # 上一次访问地址存在、上一次访问地址不是当前url地址、上一次访问地址是安全的（是指同一个域名或者IP地址）
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
            # 注册成功之后就跳转到上一次访问的地址
            return render_template("front/front_signin.html", return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                # 自动生成一个session值
                login_user(user)
                session['type'] = 'front'
                # 将登录用户保存到g对象中
                g.front_user = user
                if remember:
                    # 设置session的过期时间，默认为31天
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message="手机号或密码错误！")
        else:
            print(form.password.data, request.form.get("password"))
            print(form.errors)
            return restful.params_error(message=form.get_error())


@bp.route("/logout")
@login_required
def logout():
    """
    前台注销并将所有的cookies删除
    :return:
    """
    logout_user()
    return redirect(url_for("front.signin"))


@login_manager.user_loader
def load_user(user_id):
    """
    前台用户类必须继承UserMixin,以防用户表没有定义校验的字段，如：is_active等
    :param user_id:
    :return:
    """
    if session['type'] == 'front':
        return FrontUser.query.get(user_id)
    else:
        return CMSUser.query.get(user_id)


bp.add_url_rule("/signup", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin", view_func=SigninView.as_view("signin"))


@bp.route("/apost", methods=["GET", "POST"])
@login_required
def apost():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/front_apost.html", boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            boardId = form.boardId.data
            board = BoardModel.query.get(boardId)
            if not board:
                return restful.params_error(message="没有这个板块")
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = current_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route("/p/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template("front/front_pdetail.html", post=post)


@bp.route("/acomment", methods=["POST"])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        postId = form.postId.data
        post = PostModel.query.get(postId)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = current_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这篇帖子！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/profile")
@login_required
def profile():
    return render_template("front/front_profile.html", current_user=current_user)
