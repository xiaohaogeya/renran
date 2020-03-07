from rest_framework.generics import ListAPIView
from .models import Banner, Nav
from .serializers import BannerModelSerializer, NavModelSerializer
from datetime import datetime


class BannerListAPIView(ListAPIView):

    queryset = Banner.objects.filter(
        is_show=True,
        is_delete=True,
        start_time__lte=datetime.now(),
        end_time__gte=datetime.now()
    ).order_by("orders", "-id")[:5]
    serializer_class = BannerModelSerializer

class NavFooterListAPIView(ListAPIView):
    queryset = Nav.objects.filter(
        is_show=True,
        is_delete=False,
        option=1,
        pid=None
    ).order_by("orders", "-id")[:8]
    serializer_class = NavModelSerializer

class NavHeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(
        is_show=True,
        is_delete=False,
        option=1,
        pid=None
    ).order_by("orders", "-id")[:8]
    serializer_class = NavModelSerializer