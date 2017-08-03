from app.information.rss.worker import get_articles_by_url, get_site_info, insert_site
from app.model.info import SiteType, WebSite, Article


def validate_url(url):
    articles = get_articles_by_url(url)
    if articles:
        return True
    return False


def add_site(url, site_type_id):
    feeds = get_site_info(url)
    site_name = feeds.feed.get('title', '')
    site_url = feeds.feed.get('link', '')
    site_desc = feeds.feed.get('description', '')

    insert_site(url, site_name, site_url, site_desc, "rss", site_type_id)


def get_site_type():
    return SiteType.query.all()


def get_all_rssed_site():
    rssed_sites = WebSite.query.filter_by(sub_type='rss').all()
    return rssed_sites


def get_articles_latest():
    articles = Article.query.order_by(Article.create_time).limit(10).all()
    return articles


def get_hot_website():
    hotsites = WebSite.query.limit(10).all()
    return hotsites
