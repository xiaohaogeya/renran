from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from .models import ArticleImageModel, ArticleCollectionModel, \
    ArticleModel, SpecialModel, ArticlePostLogModel, SpecialManagerModel, SpecialArticleModel
from .serializers import ArticleImageModelSerializer, \
    ArticleCollectionModelSerializer, \
    ArticleModelSerializer, \
    SpecialModelSerializer, ArticleInfoModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from users.models import User
from renranapi.utils.tablestore import TableStore


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
    """我管理的专题列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        article_id = request.query_params.get("article_id")
        manage_list = SpecialManagerModel.objects.filter(user=user)
        data = []
        for item in manage_list:
            try:
                # 查询当前专题下所有的文章是否存在当前文章
                item.special.post_article_list.get(article_id=article_id)
                is_post_status = True
            except SpecialArticleModel.DoesNotExist:
                is_post_status = False
            data.append({
                "id": item.special.id,
                "name": item.special.name,
                "image": item.special.image.url if item.special.image else "",
                "is_post": is_post_status  # 专题对于当前文章的收录状态
            })
        return Response(data)


class ArticlePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """文章投稿"""
        user = request.user
        article_id = request.data.get("article_id")
        special_id = request.data.get("special_id")
        # 验证文章是否存在
        try:
            article = ArticleModel.objects.get(user=user, pk=article_id)
        except ArticleModel.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        # 验证专题是否存在
        try:
            special = SpecialModel.objects.get(pk=special_id)
        except SpecialModel.DoesNotExist:
            return Response("对不起,当前专题不存在!", status=status.HTTP_400_BAD_REQUEST)

        # 判断当前文章是否向专题投稿
        article_post_log_list = ArticlePostLogModel.objects.filter(special=special, article=article).order_by("-id")
        # 判断是否有投稿历史
        if len(article_post_log_list) > 0:
            # 查看最后一次投稿记录的审核状态
            if article_post_log_list[0].status != 2:
                return Response("对不起,文章已经向当前专题投稿了!", status=status.HTTP_400_BAD_REQUEST)

        # 判断当前投稿人是否属于专题的管理员
        try:
            """专题管理员"""
            special_manage = SpecialManagerModel.objects.get(user=user, special=special)
            ArticlePostLogModel.objects.create(
                user=user,
                special=special,
                article=article,
                status=1,
                manager=user.id,
                post_time=datetime.now(),
                orders=0,
            )
            SpecialArticleModel.objects.create(
                special=special,
                article=article,
                orders=0
            )
        except SpecialManagerModel.DoesNotExist:
            """并非管理员"""
            ArticlePostLogModel.objects.create(
                user=user,
                special=special,
                article=article,
                status=0,
                manager=user.id,
                post_time="",
                orders=0,
            )

        except:
            return Response("投稿失败")

        return Response("投稿成功")


class ArticleInfoAPIView(RetrieveAPIView):
    """文章详情信息"""
    serializer_class = ArticleInfoModelSerializer
    queryset = ArticleModel.objects.filter(is_publish=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 访问者已经登录
        focus = 0   # 当前访问者没有登录，默认没有关注
        # 访问者已经登录
        user = request.user

        if isinstance(user, User):
            # 判断访问者是否曾经关注过作者
            author = instance.user
            # 如果访问者和文章作者是同一个人，则不存在关注
            if author.id == user.id:
                focus = -1

            # 从关系库中获取当前访问者与作者之间的关注关系
            ts = TableStore()
            data = ts.get_one(
                "user_relation_table",
                [
                    ("user_id", author.id),
                    ("follow_user_id", user.id)
                ]
            )

            if data:
                # 已经登录了并且关注了
                focus = 2
            else:
                # 已经登录了，没有关注
                focus = 1

        ret = dict(serializer.data)
        ret["focus"] = focus
        return Response(ret)


class SpecialSixListAPIView(APIView):
    """获取最近6个投稿记录的专题的名称和图片"""
    def get(self, request):
        try:
            special_list = SpecialModel.objects.all().order_by("-id").limit(6)
            data = []
            for special in special_list:
                data.append({
                    "name": special.name,
                    "id": special.id,
                    "image": special.image,
                })
            return Response(data)
        except SpecialModel.DoesNotExist:
            return Response("操作失败")


class SpecialTenListAPIView(APIView):
    """专题表中人数最多的，文章最多的10哥专题"""
    def get(self, request):
        try:
            special_list = SpecialModel.objects.all().order_by("article_count", "follow_count").limit(10)
            data = []
            for special in special_list:
                data.append({
                    "name": special.name,
                    "id": special.id,
                    "image": special.image,
                    "follow_count": special.follow_count,
                })
            return Response(data)
        except SpecialModel.DoesNotExist:
            return Response("操作失败")


class UserFocusAPIView(APIView):
    """关注和取消关注"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 关注着[粉丝]
        user = request.user

        # 作者
        author_id = request.data.get("author_id")

        try:
            User.objects.get(pk=author_id)
        except User.DoesNotExist:
            return Response("对不起,您关注的用户不存在")

        # 获取关注状态【0表示取消关注，1表示关注】
        focus = request.data.get("focus")
        ts = TableStore()
        if focus:
            """关注"""
            ret = ts.add_one(
                "user_relation_table",
                [
                    ("user_id", author_id),
                    ("follow_user_id", user.id)
                ],
                [
                    ("focus_time", datetime.now().timestamp())
                ]
            )
        else:
            """取消关注"""
            ret = ts.del_one(
                "user_relation_table",
                [
                    ("user_id", author_id),
                    ("follow_user_id", user.id)
                ]
            )

            if ret:
                return Response("操作成功")
            else:
                return Response("操作失败")







