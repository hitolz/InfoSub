from flask import abort
from flask_login import current_user
from flask_admin import Admin, AdminIndexView

from app.model.user import User, UserPlan
from app.model.info import WebSite, SiteType, Article, Tag
from app.extensions import db
from .model_view import UserModelView, PlanModelView
from .model_view import WebSiteModelView, SiteTypeModelView, ArticleModelView, ArticleTagModelView


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user and current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        print 111
        abort(404)


admin = Admin(name='InfoSub Admin', template_mode='bootstrap3', index_view=AdminView())
admin.add_view(UserModelView(User, db.session, name="User", endpoint="user_admin"))
admin.add_view(PlanModelView(UserPlan, db.session, name="Plan", endpoint="plan_admin"))

admin.add_view(WebSiteModelView(WebSite, db.session, name="Site", endpoint="site_admin", category="Site"))
admin.add_view(SiteTypeModelView(SiteType, db.session, name="Type", endpoint="site_type_admin", category="Site"))

admin.add_view(ArticleModelView(Article, db.session, name="Article", endpoint="article_admin", category="Article"))
admin.add_view(ArticleTagModelView(Tag, db.session, name="Tag", endpoint="article_tag_admin", category="Article"))
