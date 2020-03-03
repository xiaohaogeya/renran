from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from urllib.parse import urlencode
from urllib.request import urlopen
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










