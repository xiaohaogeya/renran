from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
from datetime import datetime


class BannerListAPIView(ListAPIView):

    queryset = Banner.objects.filter(
        is_show=True,
        is_delete=True,
        start_time__lte=datetime.now(),
        end_time__gte=datetime.now()
    ).order_by("orders", "-id")[:5]
    serializer_class = BannerModelSerializer