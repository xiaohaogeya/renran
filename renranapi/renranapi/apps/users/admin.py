from django.contrib import admin

# Register your models here.
from .models import User
class UserModelAdmin(admin.ModelAdmin):
    """用户模型管理类"""
    # 按时间不同进行展示数据列表
    date_hierarchy = "last_login"

    # 设置列表页的展示字段
    list_display = ["id", "nickname", "username", "last_login", "is_superuser", "email", "my_mobile"]

    # 设置默认排序字段，字段前面加上-号表示倒叙排列
    ordering = ["-id"]

    # 下方控制栏是否显示,默认False表示隐藏
    actions_on_bottom = True

    # 上方控制栏是否显示,默认False表示隐藏
    actions_on_top = True

    # 过滤器,按指定字段的不同值进行展示
    list_filter = ["is_superuser"]

    # 搜索内容
    search_fields = ["username"]

    # 详情页中的展示字段,exclude作用与fields相反
    fields = ("nickname", "username", "mobile")

    # 设置字段
    readonly_fields = ["nickname"]

    # 字段集,fieldsets和fields只能使用其中一个
    # fieldsets = (
    #     ("必填项",{
    #         "fields": ('nickname', 'username')
    #     }),
    #     ("可选项",{
    #         # 折叠样式
    #         "classes": ("collapse"),
    #         "fields": ("mobile", )
    #     })
    # )

    def my_mobile(self, obj):
        """
        自定义字段的值,不能与模型同名
        :param obj: 当前模型
        :return: 前端列表显示的值
        """
        if obj.mobile:
            return obj.mobile[:3] + "* * * *" + obj.mobile[-3:]
        return None

    # 自定义字段空值的时候,填补的默认值
    my_mobile.empty_value_display = "暂无"

    # 自定义字段的描述信息
    my_mobile.short_description = "手机号码"

    # 自定义字段点击时使用那个字段作为排序条件
    my_mobile.admin_order_field = "mobile"

    def save_model(self, request, obj, form, change):
        """当站点保持当前模型时"""
        print("添加或修改了模型信息")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """当站点删除当前模型时"""
        print("删除了该模型信息")
        super().delete_model(request, obj)

admin.site.register(User, UserModelAdmin)