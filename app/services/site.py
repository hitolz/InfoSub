from app.information.rss.worker import get_articles_by_url


def validate_url (url):
    articles = get_articles_by_url(url)
    if articles:
        return True
    return False


