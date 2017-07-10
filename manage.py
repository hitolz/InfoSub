import os
from flask_script import Manager, Server, Shell

from app import create_app, db

RUNTIME = os.getenv("RUNTIME", "DEFAULT")
app = create_app(RUNTIME)
manager = Manager(app)


def make_shell_context():
    return {
        "db": db,
        "app": app,
    }

manager.add_command("runserver", Server(host="0.0.0.0", port=5000, use_debugger=app.config.get("DEBUG")))

banner = """
.___        _____      _________    ___.
|   | _____/ ________ /   _____/__ _\_ |__
|   |/    \   __/  _ \\\\_____  \|  |  | __ \\
|   |   |  |  |(  <_> /        |  |  | \_\ \\
|___|___|  |__| \____/_______  |____/|___  /
         \/                  \/          \/
-----------------------------------------------
ipython model. Just For Fun!
"""
manager.add_command("shell", Shell(banner=banner, make_context=make_shell_context))


@manager.command
def initdb():
    """
    init database, create all tables, create user plan and create admin.
    """
    print("init database...")
    try:
        from app.model.user import UserPlan, User, PlanUsage
        from app.model.info import WebSite, Article, SiteType, Tag, tags
        from app.model.subscribe import UserSub
        db.create_all()
    except Exception as e:
        print e

    try:
        init_user()
    except Exception:
        pass

    print "finish."


def init_user():
    print("create user plan...")
    from app.model.user import User, UserPlan
    UserPlan("trial_plan", "subscription", 5)
    UserPlan("primary_plan", "subscription", 100)
    UserPlan("intermediate_plan", "subscription", 500)
    UserPlan("advanced_plan", "subscription", 2000)
    admin_plan = UserPlan("internal_plan", "subscription", 5000)

    print("create admin...")
    admin = User("admin", "admin@updev.cn", "admin")
    admin.set_role("admin")
    admin.set_plans([admin_plan])
    print("username: {}, email: {}, password: {}".format(admin.username, admin.email, "admin"))


if __name__ == "__main__":
    manager.run()

