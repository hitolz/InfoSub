from flask import render_template
from app.information import info_blueprint
from flask_login import login_required

from app.information.form.site_form import SiteForm


@info_blueprint.route('/site', methods=["POST", "GET"])
@login_required
def site_info():
    form = SiteForm()
    if form.validate_on_submit():
        pass
    return render_template('sub_site.html', form=form)
