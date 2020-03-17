import xadmin

from .models import ArticleCollectionModel
from .models import SpecialModel
from .models import ArticleModel
from .models import SpecialArticleModel
from .models import SpecialManagerModel
from .models import SpecialFocusModel
from .models import SpecialCollectionModel
from .models import ArticleImageModel


class ArticleCollectionModelAdmin(object):
    list_display = ["id", "name"]


xadmin.site.register(ArticleCollectionModel, ArticleCollectionModelAdmin)


class SpecialModelAdmin(object):
    """专题模型管理类"""
    list_display = ["id", "name"]


xadmin.site.register(SpecialModel, SpecialModelAdmin)


class ArticleModelAdmin(object):
    list_display = ["id", "name"]


xadmin.site.register(ArticleModel, ArticleModelAdmin)


class SpecialArticleModelAdmin(object):
    """专题文章模型管理类"""
    list_display = ["id", "name"]


xadmin.site.register(SpecialArticleModel, SpecialArticleModelAdmin)


class SpecialManagerModelAdmin(object):
    """专题管理员模型管理类"""
    list_display = ["id", "name"]


xadmin.site.register(SpecialManagerModel, SpecialManagerModelAdmin)


class SpecialFocusModelAdmin(object):
    list_display = ["id", "name"]


xadmin.site.register(SpecialFocusModel, SpecialFocusModelAdmin)


class SpecialCollectionModelAdmin(object):
    list_display = ["id", "name"]


xadmin.site.register(SpecialCollectionModel, SpecialCollectionModelAdmin)


class ArticleImageModelAdmin(object):
    list_display = ["id", "name"]


xadmin.site.register(ArticleImageModel, ArticleImageModelAdmin)
