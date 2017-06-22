import os
from flask_script import Manager, Server

from app import create_app, db


RUNTIME = os.getenv("RUNTIME", "DEFAULT")
app = create_app(RUNTIME)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=5000, use_debugger=app.config.get("DEBUG")))


@manager.command
def initdb():
    """
    init database, create all tables, create user plan and create admin.
    """
    print("init database...")
    try:
        from app.model.user import UserPlan, User, PlanUsage
        db.create_all()
    except Exception as e:
        print e

    print("create user plan...")
    from app.model.user import User, UserPlan
    db.session.add(UserPlan("trial_plan", "subscription", 5))
    db.session.add(UserPlan("primary_plan", "subscription", 100))
    db.session.add(UserPlan("intermediate_plan", "subscription", 500))
    db.session.add(UserPlan("advanced_plan", "subscription", 2000))
    db.session.add(UserPlan("internal_plan", "subscription", 5000))

    print("create admin...")
    admin = User("admin", "admin@updev.cn", "admin")
    admin.set_role("admin")
    db.session.add(admin)
    db.session.commit()
    print("username: {}, email: {}, password: {}".format(admin.username, admin.email, "admin"))

    print "finish."

if __name__ == "__main__":
    manager.run()
