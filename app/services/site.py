from app.information.rss.worker import get_articles_by_url, get_site_info, insert_site


def validate_url(url):
    articles = get_articles_by_url(url)
    if articles:
        return True
    return False


def add_site(url):
    feeds = get_site_info(url)
    site_name = feeds.feed.title
    site_url = feeds.feed.link
    site_desc = feeds.feed.description

    insert_site(url, site_name, site_url, site_desc)
