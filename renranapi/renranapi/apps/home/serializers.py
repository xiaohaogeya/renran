from rest_framework import serializers
from .models import Banner, Nav


class BannerModelSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""
    class Meta:
        model = Banner
        fields = ["image", "link", "is_http", "note"]


class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Nav
        fields = ["name", "link", "is_http", "son_list"]