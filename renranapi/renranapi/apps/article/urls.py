from django.urls import path, re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("image/", views.ImageAPIView.as_view()),
    path("collection/", views.MyCollectionListAPIView.as_view()),
    path("collect/", views.CollectionCreateAPIView.as_view()),
    re_path(r"^collect/(?P<pk>\d+)/$", views.CollectionUpdateOrDeleteAPIView.as_view()),
    path("", views.ArticleOfCollectionViewSet.as_view({"get": "list"})),
    re_path(r"^public/(?P<pk>\d+)/$", views.ArticlePublicStatusAPIView.as_view()),
    re_path(r"^move/(?P<pk>\d+)/$", views.ArticleChangeCollection.as_view()),
    re_path(r"^interval/(?P<pk>\d+)/$", views.ArticleIntervalAPIView.as_view()),
    re_path(r"^delete/(?P<pk>\d+)/$", views.ArticleDeleteAPIView.as_view()),
    re_path(r"^save/(?P<pk>\d+)/$", views.ArticleUpdateAPIView.as_view()),
    path("special/list/", views.SpecialListAPIView.as_view()),
    path("post/", views.ArticlePostAPIView.as_view()),
    re_path(r"^(?P<pk>\d+)/$", views.ArticleInfoAPIView.as_view()),
    path("six/special/", views.SpecialSixListAPIView.as_view()),
    path("ten/special/", views.SpecialTenListAPIView.as_view()),
    path("focus/", views.UserFocusAPIView.as_view()),
]
