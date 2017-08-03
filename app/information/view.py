from flask import render_template
from app.information import info_blueprint
from flask_login import login_required

from app.information.form.site_form import SiteForm
from app.services.site_service import add_site, get_site_type, get_all_rssed_site, get_articles_latest, get_hot_website


@info_blueprint.route('/site', methods=["POST", "GET"])
@login_required
def site_info():
    form = SiteForm()
    form.sub_type.choices = [(t.type_id, t.type_name) for t in get_site_type()]

    if form.validate_on_submit():
        print "S   = %s " % form.rss_url.data
        print "sub_type   = %s " % form.sub_type.data
        site = add_site(form.rss_url.data, form.sub_type.data)

    return render_template('sub_site.html', rssed_sites=get_all_rssed_site(), form=form, articles=get_articles_latest(), hotsites=get_hot_website())
