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
    article_url = db.Column(db.String(255))
    article_desc = db.Column(db.Text)
    article_content = db.Column(db.Text)
    site_id = db.Column(db.String(64), db.ForeignKey('web_site.site_id'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('articles', lazy='dynamic'))
    create_time = db.Column(db.DateTime)

    def __init__(self, article_title='', article_url='', article_desc='',
                 article_content='', site_id=None, *args, **kwargs):
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

    def __unicode__(self):
        return u"Article: {}".format(self.article_title)


class Tag(db.Model):
    tag_id = db.Column(db.String(64), primary_key=True)
    tag_name = db.Column(db.String(128))
    frequency = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime)

    def __init__(self, tag_name='', *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.tag_id = str(uuid.uuid4())
        self.tag_name = tag_name
        self.create_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def __unicode__(self):
        return u"Tag: {}".format(self.tag_name)

    def add_frequency(self):
        self.frequency += 1
        db.session.add(self)
        db.session.commit()


class WebSite(db.Model):
    site_id = db.Column(db.String(64), primary_key=True)
    site_url = db.Column(db.String(64))
    site_name = db.Column(db.String(50))
    site_desc = db.Column(db.String(255))
    site_type_id = db.Column(db.String(64), db.ForeignKey('site_type.type_id'), index=True)

    sub_type = db.Column(db.String(20))
    rss_url = db.Column(db.String(128))
    spider_name = db.Column(db.String(64))

    articles = db.relationship('Article', backref='site', lazy='dynamic')
    create_time = db.Column(db.DateTime)
    last_sub_time = db.Column(db.DateTime)

    def __init__(self, rss_url='' ,site_url='', site_name='', site_desc='', sub_type='rss', *args, **kwargs):
        super(WebSite, self).__init__(*args, **kwargs)
        self.site_id = str(uuid.uuid4())
        self.site_url = site_url
        self.site_name = site_name
        self.site_desc = site_desc
        self.rss_url = rss_url
        self.sub_type = 'rss'

        self.create_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def set_site_type(self, site_type):
        self.site_type_id = site_type.type_id
        db.session.add(self)
        db.session.commit()

    def __unicode__(self):
        return u"Web Site {}: {}".format(self.site_name, self.site_url)

    def sub_success(self):
        self.last_sub_time = datetime.now()
        db.session.add(self)
        db.session.commit()


class SiteType(db.Model):
    type_id = db.Column(db.String(64), default=lambda: str(uuid.uuid4()), primary_key=True)
    type_name = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    sites = db.relationship('WebSite', backref='site_type',
                            lazy='dynamic')

    def __init__(self, type_name='', *args, **kwargs):
        super(SiteType, self).__init__(*args, **kwargs)
        self.type_id = str(uuid.uuid4())
        self.type_name = type_name
        self.create_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def set_sites(self, sites):
        self.sites = sites
        db.session.add(self)
        db.session.commit()

    def __unicode__(self):
        return u"Site Type: {}".format(self.type_name)
