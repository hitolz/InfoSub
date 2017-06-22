import uuid
from datetime import datetime, timedelta

from app.extensions import db


class UserSub(db.Model):
    us_id = db.Column(db.String(64), default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.user_id'), index=True)
    site_id = db.Column(db.String(64), db.ForeignKey('web_site.site_id'))
    use_quota = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)

    def __init__(self, user_id, site_id):
        self.user_id = user_id
        self.site_id = site_id
        self.use_quota = 1
        self.create_time = datetime.now()


