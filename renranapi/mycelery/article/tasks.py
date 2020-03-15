from mycelery.main import app
from article.models import ArticleModel
from datetime import datetime


@app.task(name="interval_pub_article")
def interval_pub_article():
    """定时发布文章"""
    article_list = ArticleModel.objects.filter(pub_date__lte=datetime.now()).exclude(pub_date=None)
    for article in article_list:
        article.pub_date = None
        article.is_public = True
        article.save()
