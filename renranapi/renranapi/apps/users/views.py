from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.conf import settings
from urllib.parse import urlencode
from urllib.request import urlopen
from .utils import get_user_by_data
from .serializers import UserCreateModelSerializer
from .models import User
import json
import logging
loger = logging.getLogger("django")


class CaptchaAPIView(APIView):

    def post(self, request):
        AppSecretKey = settings.TENCENT_CAPTCHA.get("App_Secret_Key")
        appid = settings.TENCENT_CAPTCHA.get("APPID")
        Ticket = request.data.get("ticket")
        Randstr = request.data.get("randstr")
        UserIP = request._request.META.get("REMOTE_ADDR")
        params = {
            "aid": appid,
            "AppSecretKey": AppSecretKey,
            "Ticket": Ticket,
            "Randstr": Randstr,
            "UserIP": UserIP
        }
        params = urlencode(params)
        ret = self.txrequest(AppSecretKey, params)
        return Response({
            "message": ret,
            "randstr": Randstr
        })

    def txrequest(self, params, m = "GET"):
        url = "https://ssl.captcha.qq.com/ticket/verify"
        if m == "GET":
            f = urlopen("%s?%s" % (url, params))
        else:
            f = urlopen(url, params)
        content = f.read()
        res = json.loads(content)
        if not res:
            return False
        else:
            error_code = res["response"]
            if error_code == "1":
                return True
            else:
                # 记录日志
                loger.error(f"验证接口异常!%s:%s" % (res["response"], res["err_msg"]))
                return False

class CheckMobileAPIView(APIView):
    def get(self, request, mobile):
        user = get_user_by_data(mobile = mobile)
        if user is None:
            return Response({
                "err_msg": "ok",
                "err_status": 1
            })
        else:
            return Response({
                "err_msg": "当前手机号已被注册",
                "err_status": 0
            },status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(CreateAPIView):
    """添加用户"""
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer






