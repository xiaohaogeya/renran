from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.conf import settings
from django_redis import get_redis_connection
from urllib.parse import urlencode
from urllib.request import urlopen
from .utils import get_user_by_data
from .serializers import UserCreateModelSerializer
from .models import User
from renranapi.settings import constants
import random
import json
import logging
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
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

    def txrequest(self, appkey, params, m = "GET"):
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

class SMSCodeAPIView(APIView):
    """短信验证码"""
    def get(self, request, mobile):
        # 1.验证数据
        redis = get_redis_connection("sms_code")
        result = redis.get("interval_%s" % mobile)
        print(mobile)
        if result:
            return Response({
                "message": "短信发送中,请留意您的手机,请勿频繁操作",
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2.生成随机短信验证码
        sms_code = "%04d" % random.randint(0, 9999)

        # 3.发送短信验证码
        # 3.1 声明一个和celery一模一样的任务函数,但是我们可以导包来解决
        from mycelery.sms.tasks import send_sms
        # 3.2 调用任务函数,发布任务
        send_sms.delay(mobile=mobile, sms_code=sms_code)

        # 4.保存短信验证码到redis中
        # 4.1 创建管道对象
        pipe = redis.pipeline()
        # 4.2 开启事务
        pipe.multi()
        # 4.3 设置事务中的相关命令
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        pipe.setex("interval_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")
        # 4.4 提交事务
        pipe.execute()

        # 5.返回操作结果
        return Response({"message": "短信已经发送,请留意您的手机"})





