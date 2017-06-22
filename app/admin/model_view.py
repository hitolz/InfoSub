# coding=utf-8
from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.util.user_display import user_display, plan_type_display


class InfoSubModelView(ModelView):

    def is_accessible(self):
        return True
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class UserModelView(InfoSubModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', 'email']
    can_delete = False

    form_choices = {
        'role': [
            ('trial_user', user_display['trial_user']),
            ('pay_user', user_display['pay_user']),
            ('internal_user', user_display['internal_user']),
            ('admin', user_display['admin']),
        ]
    }

    form_widget_args = {
        'password': {
            'type': "password",
        },
        'email': {
            'type': "email",
        }
    }

    column_labels = dict(
        username=u'用户名',
        email=u'电子邮箱',
        password=u'密码',
        role=u'角色',
        plans=u'套餐',
        is_active=u'激活',
        create_time=u'创建时间',
    )


class PlanModelView(InfoSubModelView):
    can_delete = False

    column_labels = dict(
        plan_name=u"套餐名称",
        plan_type=u"套餐类型",
        plan_quota=u"可用资源",
        create_time=u"创建时间",
        users=u"用户",
    )

    form_choices = {
        'plan_type': [
            ('subscription', plan_type_display['subscription']),
        ]
    }


class WebSiteModelView(InfoSubModelView):
    pass


class SiteTypeModelView(InfoSubModelView):
    pass


class ArticleModelView(InfoSubModelView):
    pass


class ArticleTagModelView(InfoSubModelView):
    pass


