from app.model.user import User, UserPlan
from app.util.tracer import tracer_decorator, current_span


@tracer_decorator("get_user_by_email_or_name")
def get_user_by_username_or_email(username_or_email):
    user = User.query.filter_by(username=username_or_email).first()
    current_span().set_tag("username_or_email", username_or_email)
    if not user:
        user = User.query.filter_by(email=username_or_email).first()
    if not user:
        return None
    return user


@tracer_decorator("validate_username")
def validate_username(username):
    current_span().set_tag("username", username)
    if (username or "").lower() in ["admin", "administrator", "root", "user"]:
        current_span().log_event("wrong username: Illegal username", payload=dict(username=username))
        return False
    if len(username) > 60:
        current_span().log_event("wrong username: too long", payload=dict(username=username))
        return False
    user = User.query.filter_by(username=username).first()
    if not user:
        return True
    current_span().log_event("wrong username: used", payload=dict(username=username))
    return False


@tracer_decorator("validate_email")
def validate_email(email):
    current_span().set_tag("email", email)
    if len(email) > 120:
        current_span().log_event("wrong email: too long", payload=dict(email=email))
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return True
    current_span().log_event("wrong email: too long", payload=dict(email=email))
    return False


@tracer_decorator("create_user")
def create_user(username, email, password):
    current_span().set_tag("create_user", username)
    user = User(username=username, email=email, password=password)
    current_span().log_event("create user success", payload=dict(user_id=user.user_id, username=username, email=email))
    return user


@tracer_decorator("init_plan")
def init_user_plan(user, coupon_code):
    current_span().set_tag("user_id", user.user_id)
    coupon = None
    if coupon:
        user.set_plans([])
        user.set_role("invited_user")
    else:
        plan = UserPlan.query.filter_by(plan_name="trial_plan").first()
        user.set_plans([plan])
    current_span().log_event("init user plan success", payload=dict(
        coupon=coupon_code,
        rule=user.role,
    ))

