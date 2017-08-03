from flask import render_template

from app.view import view_blueprint




@view_blueprint.route("/")
def home():
    return render_template("index_base.html")


@view_blueprint.route("/site")
def site():
    return render_template("web_site.html")


@view_blueprint.route("/wechat")
def wechat():
    return render_template("wechat.html")


@view_blueprint.route("/weibo")
def weibo():
    return render_template("weibo.html")


@view_blueprint.route("/tags")
def tags():
    return render_template("tags.html")


@view_blueprint.route("/about")
def about():
    return render_template("about.html")
