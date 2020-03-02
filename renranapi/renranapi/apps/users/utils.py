from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
def jwt_response_payload_handler(token, user = None, request = None):
    """jwt自定义响应载荷"""
    return {
        "token": token,
        "id": user.id,
        "username": user.username,
        "avatar": "" if not user.avatar else user.avatar.url,
        "nickname": user.nickname,
    }

def get_user_by_account(account):
    """
    通过账户信息获取用户模型
    :param account: username或者是手机号或者是邮箱，获取其他的唯一字段的信息
    :return: user模型
    """
    User = get_user_model()
    try:
        return User.objects.get(Q(mobile= account) | Q(username= account) | Q(email= account) | Q(qq_number = account))
    except User.DoesNotExist:
        return None

class AccountModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user