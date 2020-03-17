from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from .models import ArticleImageModel, ArticleCollectionModel, ArticleModel, SpecialModel
from .serializers import ArticleImageModelSerializer, \
    ArticleCollectionModelSerializer, \
    ArticleModelSerializer, \
    SpecialModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.views import APIView


class ImageAPIView(CreateAPIView):
    """保存文章图片"""
    queryset = ArticleImageModel.objects.all()
    serializer_class = ArticleImageModelSerializer


class CollectionCreateAPIView(CreateAPIView):
    """添加文集"""
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来


class CollectionUpdateOrDeleteAPIView(UpdateAPIView, DestroyAPIView):
    """修改文集或删除文集"""
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


class ArticlePublicStatusAPIView(APIView):
    """切换文章的发布状态"""
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来

    def put(self, request, pk):
        try:
            article = ArticleModel.objects.get(pk=pk)
        except ArticleModel.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        is_public = request.data.get("is_public")
        article.is_publish = not not is_public
        article.pub_date = None
        article.save()
        return Response("操作成功")


class ArticleChangeCollection(APIView):
    """移动文章"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = ArticleModel.objects.get(pk=pk)
        except ArticleModel.DoesNotExist:
            return Response("对不起,当前文章不存在", status=status.HTTP_400_BAD_REQUEST)
        collection_id = request.data.get("collection_id")
        article.collection_id = int(collection_id)
        article.save()
        return Response("操作成功")


class ArticleIntervalAPIView(APIView):
    """定时发布文章"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = ArticleModel.objects.get(pk=pk)
        except ArticleModel.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)
        pub_date = request.data.get("pub_date")
        article.pub_date = pub_date
        article.save()
        return Response("操作成功!")


class ArticleDeleteAPIView(DestroyAPIView):
    """删除文章"""
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登录用户才能访问过来


class ArticleUpdateAPIView(APIView):
    """文章标题和内容修改保存"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = ArticleModel.objects.get(pk=pk)
        except ArticleModel.DoesNotExist:
            return Response("对不起,当前文章不存在", status=status.HTTP_400_BAD_REQUEST)

        article.name = request.data.get("name")
        article.content = request.data.get("content")
        article.render = request.data.get("render")
        article.save()
        return Response("操作成功")


class SpecialListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        manage_list = SpecialModel.objects.filter(user=user)
        data = []
        for item in manage_list:
            data.append({
                "id": item.special.id,
                "name": item.special.name,
                "image": item.special.image.url if item.special.image else "",
            })
        return Response(data)
