import feedparser
import ssl
from urlparse import urlparse

from app.model.info import *

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def get_all_site():
    sites = WebSite.query.filter_by(sub_type='rss').all()
    for site in sites:
        sub_this_site(site)


def sub_this_site(site):
    feeds = feedparser.parse(site.rss_url)
    for feed in feeds['entries']:
        article_title = feed.get('title')
        article_link = feed.get('link')
        article_desc = feed.get('description', '')
        article_content = feed.get('content', '')[0]['value']
        into_article(article_title, article_link, article_desc, article_content, site.site_id)
    if len(feeds['entries']) > 0:
        site.sub_success()


def into_article(article_title, article_link, article_desc, article_content, site_id):
    link = urlparse(article_link)
    url = link.netloc + link.path

    if Article.query.filter(Article.article_url.endswith(url)).first():
        return

    article = Article(
        article_title=article_title,
        article_url=article_link,
        article_desc=article_desc,
        article_content=article_content,
        site_id=site_id
    )


if __name__ == "__main__":
    from manage import app

    with app.app_context() as app:
        get_all_site()
