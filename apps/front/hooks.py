from flask import render_template

from apps.front import bp


@bp.errorhandler
def page_not_found(error):
    return render_template("front/front_404.html"), 404
