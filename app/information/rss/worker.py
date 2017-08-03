# -*- encoding:utf-8 -*-
import feedparser
import ssl
from urlparse import urlparse
from textrank4zh import TextRank4Keyword, TextRank4Sentence

from app.model.info import *

import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def into_tag(item):
    if item.weight < 0.02:
        return
    print(item.word, item.weight)
    tag = Tag.query.filter_by(tag_name=item.word).first()
    if tag:
        tag.add_frequency()
        return
    return Tag(tag_name=item.word)


def extract_tag(content):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=content, lower=True, window=2)

    print('keywords')
    tags = []
    for item in tr4w.get_keywords(20, word_min_len=3):
        tag = into_tag(item)
        if tag:
            tags.append(tag)
    return tags


def get_all_site():
    sites = WebSite.query.filter_by(sub_type='rss').all()
    for site in sites:
        sub_this_site(site)


def get_articles_by_url(rss_url):
    feeds = feedparser.parse(rss_url)
    return feeds['entries']


def get_site_info(rss_url):
    print rss_url
    feeds = feedparser.parse(rss_url)
    return feeds


def insert_site(rss_url, site_name, site_url, site_desc, sub_type,site_type_id):

    if WebSite.query.filter(WebSite.rss_url.endswith(rss_url)).first():
        return

    print "rss_url = %s " % rss_url
    print "site_name = %s " % site_name
    print "site_url = %s " % site_url
    print "site_desc = %s " % site_desc
    print "sub_type = %s" % sub_type
    site = WebSite(rss_url, site_url, site_name, site_desc, sub_type)
    site.set_site_type(site_type_id)
    print "insert success"


def sub_this_site(site):
    articles = get_articles_by_url(site.rss_url)
    print site.rss_url
    for feed in articles:
        article_title = feed.get('title')
        article_link = feed.get('link')
        article_desc = feed.get('description', '')
        article_content = feed.get('content', '')[0]['value']

        into_article(article_title, article_link, article_desc, article_content, site.site_id)
    if len(articles) > 0:
        site.sub_success()


def into_article(article_title, article_link, article_desc, article_content, site_id):
    link = urlparse(article_link)
    url = link.netloc + link.path

    if Article.query.filter(Article.article_url.endswith(url)).first():
        return
    tags = extract_tag(article_content)
    article = Article(
        article_title=article_title,
        article_url=article_link,
        article_desc=article_desc,
        article_content=article_content,
        site_id=site_id
    )
    article.set_tags(tags)


if __name__ == "__main__":
    from manage import app

    with app.app_context() as app:
        get_all_site()
