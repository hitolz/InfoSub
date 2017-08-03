from app.extensions import celery
from datetime import datetime
from app.information.rss.worker import get_all_site

@celery.task(name='add')
def add_together(a, b):
    print a + b
    return a + b


@celery.task
def sub(a, b):
    return a - b


@celery.task(name='opt_file')
def opt_file():
    file = open("abc.txt", "a+")
    data = "hello \n"
    now = str(datetime.now())
    file.write(data + now + "\n")
    file.flush()
    file.close()


@celery.task(name='get_article_everyday')
def get_article_everyday():
    get_all_site()
