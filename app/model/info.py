import uuid
from datetime import datetime
from app.extensions import db

tags = db.Table(
    'article_tag',
    db.Column('tag_id', db.String(64), db.ForeignKey('tag.tag_id')),
    db.Column('article_id', db.String(64), db.ForeignKey('article.article_id'))
)


class Article(db.Model):
    article_id = db.Column(db.String(64), primary_key=True)
    article_title = db.Column(db.String(255))
    article_url = db.Column(db.String(64))
    article_desc = db.Column(db.String(255))
    article_content = db.Column(db.Text)
    site_id = db.Column(db.String(64), db.ForeignKey('web_site.site_id'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('articles', lazy='dynamic'))
    create_time = db.Column(db.DateTime)

    def __init__(self, article_title='', article_url='', article_desc='', article_content='',
                 site_id='', *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.article_id = str(uuid.uuid4())
        self.article_title = article_title
        self.article_url = article_url
        self.article_desc = article_desc
        self.article_content = article_content
        self.site_id = site_id
        db.session.add(self)
        db.session.commit()

    def set_tags(self, a_tags):
        self.tags = a_tags
        db.session.add(self)
        db.session.commit()


class Tag(db.Model):
    tag_id = db.Column(db.String(64), primary_key=True)
    tag_name = db.Column(db.String(10))
    create_time = db.Column(db.DateTime)

    def __init__(self, tag_name, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.tag_id = uuid.uuid4()
        self.tag_name = tag_name
        self.create_time = datetime.now()


class WebSite(db.Model):
    site_id = db.Column(db.String(64), primary_key=True)
    site_url = db.Column(db.String(64))
    sub_id = db.Column(db.String(64))
    site_type_id = db.Column(db.String(20), db.ForeignKey('site_type.type_id'), index=True)
    articles = db.relationship('Article', backref='site',
                               lazy='dynamic')
    site_name = db.Column(db.String(50))
    site_desc = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def __init__(self, site_url, site_type, site_name, site_desc, sub_type, *args, **kwargs):
        super(WebSite, self).__init__(*args, **kwargs)
        self.site_id = str(uuid.uuid4())
        self.site_url = site_url
        self.site_type = site_type
        self.site_name = site_name
        self.site_desc = site_desc

        sub = SiteSub(self.site_id, sub_type)
        self.sub_id = sub.sub_id
        self.create_time = datetime.now()


class SiteSub(db.Model):
    sub_id = db.Column(db.String(64), primary_key=True)
    sub_type = db.Column(db.String(20))
    site_id = db.Column(db.String(64))
    rss_url = db.Column(db.String(128))
    spider_name = db.Column(db.String(64))
    create_time = db.Column(db.DateTime)
    last_sub_time = db.Column(db.DateTime)

    def __init__(self, site_id, sub_type, rss_url, spider_name, *args, **kwargs):
        super(SiteSub, self).__init__(*args, **kwargs)
        self.site_id = site_id
        self.sub_id = str(uuid.uuid4())
        self.sub_type = sub_type
        self.rss_url = rss_url
        self.spider_name = spider_name
        self.create_time = datetime.now()

    def sub_success(self):
        self.last_sub_time = datetime.now()


class SiteType(db.Model):
    type_id = db.Column(db.String(64), primary_key=True)
    type_name = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    sites = db.relationship('WebSite', backref='site_type',
                            lazy='dynamic')

    def __init__(self, type_name, *args, **kwargs):
        super(SiteType, self).__init__(*args, **kwargs)
        self.type_name = type_name
        self.create_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def set_sites(self, sites):
        self.sites = sites
        db.session.add(self)
        db.session.commit()
