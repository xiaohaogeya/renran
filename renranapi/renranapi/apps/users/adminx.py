import xadmin
from xadmin import views
from django.apps import AppConfig
from .models import User



class BaseSetting(object):
    """xadmin的基本配置"""
    # 开启主题切换功能
    enable_themes = True
    use_bootswatch = True

xadmin.site.unregister(User)
xadmin.site.register(views.BaseAdminView, BaseSetting)



class GlobalSettings(object):
    """xadmin的全局配置"""
    # 设置站点标题
    site_title = "荏苒"

    # 设置站点的页脚
    site_footer = "广州荏苒有限公司"

    # 设置菜单折叠
    menu_style = "accordion"

    # 生成图表
    data_charts = {
        "order_amount": {
            'title': '用户表',
            "x-field": "is_superuser",
            "y-field": ('username',),
            "order": ('id',)
        },
    }


xadmin.site.register(views.CommAdminView, GlobalSettings)

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"

class UsersInfoAdmin(object):
    model_icon = 'fa fa-gift'


xadmin.site.register(User, UsersInfoAdmin)