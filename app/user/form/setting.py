# coding=utf-8
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from app.services.user import validate_email


class UserInfoForm(FlaskForm):
    username = StringField(u'用户名')
    email = StringField(u'邮箱', validators=[DataRequired(u"修改邮箱不能为空")])

    def validate_email(self, field):
        print field.data
        if validate_email(field.data):
            return
        if current_user.email == field.data:
            raise ValidationError(u"邮箱未作出修改")
        raise ValidationError(u"邮箱不可用")


class UserPassEditForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired(u'请输入旧密码')])
    new_password = PasswordField(u'新密码', validators=[DataRequired(u'新密码不能为空')])
    re_new_password = PasswordField(u'再次输入')

    def validate_old_password(self, field):
        if current_user.check_password(field.data):
            return
        raise ValidationError(u"密码错误")

    def validate_new_password(self, field):
        if len(field.data) < 6:
            raise ValidationError(u"密码过于简单")
        if field.data != self.re_new_password.data:
            raise ValidationError(u"两次密码输入不一致")


class DeleteUserForm(FlaskForm):
    check_password = PasswordField(u'登录密码', validators=[DataRequired(u'登录密码不能为空')])

    def validate_check_password(self, field):
        if current_user.check_password(field.data):
            if current_user.role == "admin":
                raise ValidationError(u"管理员同学不要闹_(:з」∠)_")
            return
        raise ValidationError(u"登录密码错误")

