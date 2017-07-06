from flask import render_template
from app.information import info_blueprint
from flask_login import login_required

from app.information.form.site_form import SiteForm
from app.services.site import add_site


@info_blueprint.route('/site', methods=["POST", "GET"])
@login_required
def site_info():
    form = SiteForm()
    if form.validate_on_submit():
        print "S   = %s " % form.rss_url.data
        site = add_site(form.rss_url.data)
    return render_template('sub_site.html', form=form)

