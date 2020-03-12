from rest_framework import serializers
from .models import ArticleImageModel, ArticleCollectionModel


class ArticleImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImageModel
        fields = ["image"]

    def create(self, validated_data):
        instance = ArticleImageModel.objects.create(
            image=validated_data.get("image"),
            group=1
        )

        return instance


class ArticleCollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCollectionModel
        fields = ["name"]

    def validate(self, attrs):
        # 验证当前用户的文集是否同名
        user = self.context["request"].user
        name = attrs.get("name")
        try:
            ArticleCollectionModel.objects.get(user=user, name=name)
            raise serializers.ValidationError("对不起,当前文集您已经创建!")
        except ArticleCollectionModel.DoesNotExist:
            pass

    def create(self, validated_data):
        user = validated_data.get("user")
        name = validated_data.get("name")
        try:
            collection = ArticleCollectionModel.objects.create(user=user, name=name)
        except:
            raise serializers.ValidationError("对不起,当前文集您已经创建了!")
        return collection
