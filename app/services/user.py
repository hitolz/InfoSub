from app.model.user import User, UserPlan


def get_user_by_username_or_email(username_or_email):
    user = User.query.filter_by(username=username_or_email).first()
    if not user:
        user = User.query.filter_by(email=username_or_email).first()
    if not user:
        return None
    return user


def validate_username(username):
    if (username or "").lower() in ["admin", "administrator", "root", "user"]:
        return False
    if len(username) > 60:
        return False
    user = User.query.filter_by(username=username).first()
    if not user:
        return True
    return False


def validate_email(email):
    if len(email) > 120:
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return True
    return False


def create_user(username, email, password):
    user = User(username=username, email=email, password=password)
    plan = UserPlan.query.filter_by(plan_name="trial_plan").first()
    user.set_plans([plan])
    return user

