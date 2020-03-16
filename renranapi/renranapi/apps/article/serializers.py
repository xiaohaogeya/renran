from rest_framework import serializers
from .models import ArticleImageModel, ArticleCollectionModel, ArticleModel
from datetime import datetime


class ArticleImageModelSerializer(serializers.ModelSerializer):
    """文章图片的序列化器"""

    class Meta:
        model = ArticleImageModel
        fields = ["image"]

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        instance = ArticleImageModel.objects.create(
            image=validated_data.get("image"),
            orders=0,
            user=user_id
        )
        instance.group = str(instance.image).split("/")[0]
        instance.save()
        return instance


class ArticleCollectionModelSerializer(serializers.ModelSerializer):
    """文集的序列化器"""

    class Meta:
        model = ArticleCollectionModel
        fields = ["id", "name"]

    def validate_name(self, name):
        # 验证当前用户的文集是否同名
        user = self.context["request"].user
        try:
            ArticleCollectionModel.objects.get(user=user, name=name)
            raise serializers.ValidationError("对不起,当前文集您已经创建!")
        except ArticleCollectionModel.DoesNotExist:
            pass
        return name

    def create(self, validated_data):
        """保存数据"""
        try:
            collection = ArticleCollectionModel.objects.create(
                user=self.context["request"].user,
                name=validated_data.get("name"),
                orders=0
            )
        except:
            raise serializers.ValidationError("对不起,添加文集失败了!")
        return collection

    def update(self, instance, validated_data):
        """修改数据"""
        instance.name = validated_data.get("name")
        instance.save()
        return instance


class ArticleModelSerializer(serializers.ModelSerializer):
    """文章的序列化器"""
    position = serializers.BooleanField(write_only=True, label="添加文章的位置")

    class Meta:
        model = ArticleModel
        fields = ["id", "name", "content", "collection", "position"]
        read_only_fields = ["id", "name", "content"]

    def create(self, validated_data):
        """保存数据"""
        try:
            article = ArticleModel.objects.create(
                name=datetime.strftime(datetime.now(), "%Y-%m-%d"),
                collection=validated_data.get("collection"),
                user=self.context["request"].user,
                orders=0
            )
        except:
            raise serializers.ValidationError("对不起,添加文章失败")
        position = validated_data.get("position")
        if position:
            """如果是下方添加,则把id设置为orders为id"""
            article.orders = article.id
            article.save()
        return article
