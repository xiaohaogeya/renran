from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from .models import ArticleImageModel, ArticleCollectionModel, ArticleModel
from .serializers import ArticleImageModelSerializer, ArticleCollectionModelSerializer, ArticleModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ImageAPIView(CreateAPIView):
    queryset = ArticleImageModel.objects.all()
    serializer_class = ArticleImageModelSerializer


class CollectionCreateAPIView(CreateAPIView):
    """添加文集"""
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来


class CollectionUpdateAPIView(UpdateAPIView):
    """修改文集"""
    queryset = ArticleCollectionModel.objects.all()
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来


class MyCollectionListAPIView(ListAPIView):
    """我的文集"""
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来

    def get_queryset(self):
        """重写queryset属性值"""
        user = self.request.user
        ret = ArticleCollectionModel.objects.filter(user=user).order_by("orders", "-id")
        if len(ret) < 1:
            # 当用户如果没有文集,在默认给用户创建2个文集
            collection_one = ArticleCollectionModel.objects.create(
                user=user,
                name="日记本",
                orders=1
            )
            collection_two = ArticleCollectionModel.objects.create(
                user=user,
                name="随笔",
                orders=2
            )
            ret = [
                {"id": collection_one.pk, "name": collection_one.name},
                {"id": collection_two.pk, "name": collection_two.name},
            ]
            return ret


class ArticleOfCollectionViewSet(GenericViewSet, ListAPIView, CreateAPIView):
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来

    def list(self, request, *args, **kwargs):
        collection_id = request.query_params.get("collection")
        user = request.user
        query_set = ArticleModel.objects.filter(
            is_delete=False,
            user=user,
            collection_id=collection_id
        ).order_by("orders", "-id")
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)



