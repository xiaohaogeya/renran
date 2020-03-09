from rest_framework.views import APIView
from .utils import OAuthQQ
from rest_framework.response import Response

class OAuthQQAPIView(APIView):
    def get(self, request):
        """生成QQ登录的地址"""
        # 客户端指定的状态
        state = request.query_params.get("state")
        oauth = OAuthQQ(state=state)
        url = oauth.get_auth_url()
        return Response(url)