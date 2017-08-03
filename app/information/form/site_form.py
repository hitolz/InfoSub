# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.services.site_service import validate_url


class SiteForm(FlaskForm):
    rss_url = StringField(u"rss地址", validators=[DataRequired(u"网站地址不能为空")])
    sub_type = SelectField(u"选择网站类型", choices=[],
                           validators=[DataRequired(u"类型不能为空")])

    def validate_rss_url(self, field):
        if validate_url(field.data):
            return
        raise ValidationError(u"该rss地址不可用")
