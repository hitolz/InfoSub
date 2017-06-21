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
    init database, create all tables.
    :return:
    """
    print "init database..."
    try:
        db.create_all()
    except Exception as e:
        print e
    print "finish."

