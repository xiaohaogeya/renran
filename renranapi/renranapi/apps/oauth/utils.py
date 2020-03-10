from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
import logging
import json

logger = logging.getLogger("django")

class OAuthQQ(object):
    """QQ认证辅助工具类"""
    def __init__(self, app_id=None, app_key=None, redirect_uri=None, state=None):
        self.app_id = app_id or settings.QQ_APP_ID
        self.app_key = app_key or settings.QQ_APP_KEY
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URL
        # 用于保存登录成功后的跳转页面路径
        self.state = state or settings.QQ_STATE

    def get_auth_url(self):
        """
        获取qq登录的网址
        :return: url网址路径
        """
        params = {
            "response_type": "code",
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "scope": "get_user_info",
        }
        url = "https://graph.qq.com/oauth2.0/authorize?" + urlencode(params)

        return url

    def get_access_token(self, code=None):
        """通过授权码获取临时票据access_token"""
        params = {
            "grant_type": "authorization_code",
            "client_id": self.app_id,
            "client_secret": self.app_key,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        # urlencode把字典转化成查询字符串格式
        url = "https://graph.qq.com/oauth2.0/token?" + urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            # parse_qs把字符串格式的内容转化成字典[注意⚠️：转化后的字典，值是列表格式]
            data = parse_qs(response_data)
            if data.get("access_token") != None:
                access_token = data.get("access_token")[0]
                refresh_token = data.get("refresh_token")[0]
            else:
                raise OAuthQQTokenError("code已经过期,请重新登录QQ账号")
        except:
            logger.error(f"code={data.get('code')} msg={data.get('msg')}")
            raise OAuthQQTokenError
        return access_token, refresh_token

    def get_open_id(self, access_token=None):
        """根据access_token获取openid"""
        url = "https://graph.qq.com/oauth2.0/me?access_token=" + access_token
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = json.loads(response_data[10:-4])
            openid = data.get("openid")
        except:
            logger.error(f"code={data.get('code')} msg={data.get('msg')}")
            raise OAuthQQErrorOpenID
        return openid

    def get_qq_user_info(self, access_token=None, openid=None):
        params = {
            "access_token": access_token,
            "oauth_consumer_key": self.app_id,
            "openid": openid,
        }
        url = "https://graph.qq.com/user/get_user_info?" + urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = json.loads(response_data)
        except:
            logger.error(f"code={data.get('code')} msg={data.get('msg')}")
            raise OAuthQQErrorUserInfo
        return data


class OAuthQQTokenError(Exception):
    pass

class OAuthQQErrorOpenID(Exception):
    pass

class OAuthQQErrorUserInfo(Exception):
    pass
