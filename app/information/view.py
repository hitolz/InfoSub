from flask import render_template
from app.information import info_blueprint


@info_blueprint.route('/')
def infohome():
    return render_template('subsite.html')