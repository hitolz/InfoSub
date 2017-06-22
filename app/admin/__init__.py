from flask_admin import Admin

from app.model.user import User, UserPlan, PlanUsage
from app.extensions import db
from .model_view import UserModelView, PlanModelView

admin = Admin(name='InfoSub Admin', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session, name="User", endpoint="user_admin"))
admin.add_view(PlanModelView(UserPlan, db.session, name="Plan", endpoint="plan_admin"))
