from django.urls import path, re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("uploading/", views.ImageAPIView.as_view()),
    path("collection/", views.MyCollectionListAPIView.as_view()),
    path("collect/", views.CollectionCreateAPIView.as_view()),
    re_path(r"^collect/(?P<pk>\d+)/$", views.CollectionUpdateOrDeleteAPIView.as_view()),
    path("", views.ArticleOfCollectionViewSet.as_view({"get": "list"})),
    re_path(r"^public/(?P<pk>\d+)/$", views.ArticlePublicStatusAPIView.as_view()),
]
