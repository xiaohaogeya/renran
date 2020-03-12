from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from .models import ArticleImageModel, ArticleCollectionModel
from .serializers import ArticleImageModelSerializer, ArticleCollectionModelSerializer
from rest_framework.permissions import IsAuthenticated


class ImageAPIView(CreateAPIView):
    queryset = ArticleImageModel.objects.all()
    serializer_class = ArticleImageModelSerializer


class CollectionAPIView(CreateAPIView):
    """添加文集"""
    queryset = ArticleCollectionModel.objects.all()
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]