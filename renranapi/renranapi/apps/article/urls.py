from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("uploading/", views.ImageAPIView.as_view()),
    path("collection/", views.CollectionAPIView.as_view()),
]