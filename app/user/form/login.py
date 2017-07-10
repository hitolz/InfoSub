# coding=utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.validators import ValidationError

from app.services.user import get_user_by_username_or_email, validate_email, validate_username
from app.util.captcha_tool import Captcha


class LoginForm(FlaskForm):
    username_or_email = StringField(u"用户名或注册邮箱", validators=[DataRequired(u"登录名不能为空")])
    password = PasswordField(u"密码", validators=[DataRequired(u"密码不能为空")])
    remember = BooleanField(u"记住我", default=False)
    captcha_code = StringField(u"验证码")
    captcha_id = HiddenField()

    def validate_password(self, field):
        user = get_user_by_username_or_email(self.username_or_email.data)
        if user and user.is_active and user.check_password(field.data):
            return
        raise ValidationError(u"用户名或密码错误")

    def validate_captcha_code(self, field):
        if current_app.config.get("DEBUG"):
            return
        if self.captcha_id.data:
            captcha = Captcha.get_by_captcha_id(self.captcha_id.data)
            if captcha.validate(field.data):
                return
        raise ValidationError(u"验证码错误")


class RegisterForm(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired(u"用户名不能为空")])
    email = StringField(u"邮箱", validators=[DataRequired(u"邮箱不能为空"), Email(u"邮箱格式非法")])
    password = PasswordField(u"登录密码", validators=[
        DataRequired(u"登录密码不能为空"),
        Length(min=6, max=18, message=u"密码长度应在 6~18 位"),
    ])
    re_password = PasswordField(u"重复密码", validators=[EqualTo("password", u"两次密码输入不一致")])
    coupon = StringField(u"邀请码")
    captcha_code = StringField(u"验证码")
    captcha_id = HiddenField()

    def validate_username(self, field):
        if validate_username(field.data):
            return
        raise ValidationError(u"用户名不可用")

    def validate_email(self, field):
        if validate_email(field.data):
            return
        raise ValidationError(u"邮箱不可用")

    def validate_captcha_code(self, field):
        if current_app.config.get("DEBUG"):
            return
        if self.captcha_id.data:
            captcha = Captcha.get_by_captcha_id(self.captcha_id.data)
            if captcha.validate(field.data):
                return
        raise ValidationError(u"验证码错误")
