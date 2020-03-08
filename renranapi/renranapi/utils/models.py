from django.db import models

class BaseModel(models.Model):
    ICON_CHOOSE = (
        (1, "el-icon-upload"),
        (2, "el-icon-error"),
        (3, "el-icon-success"),
        (4, "el-icon-warning"),
        (5, "el-icon-sort-down"),
        (6, "el-icon-sort-up"),
        (7, "el-icon-arrow-left"),
        (8, "el-icon-circle-plus"),
        (9, "el-icon-circle-plus-outline"),
        (10, "el-icon-arrow-down"),
        (11, "el-icon-arrow-right"),
        (12, "el-icon-arrow-up"),
        (13, "el-icon-back"),
        (14, "el-icon-circle-close"),
        (15, "el-icon-date"),
        (16, "el-icon-circle-close-outline"),
        (17, "el-icon-caret-left"),
        (18, "el-icon-caret-bottom"),
        (19, "el-icon-caret-top"),
        (20, "el-icon-caret-right"),
        (21, "el-icon-close"),
        (22, "el-icon-d-arrow-left"),
        (23, "el-icon-check"),
        (24, "el-icon-delete"),
        (25, "el-icon-d-arrow-right"),
        (26, "el-icon-document"),
        (27, "el-icon-d-caret"),
        (28, "el-icon-edit-outline"),
        (29, "el-icon-download"),
        (30, "el-icon-goods"),
        (31, "el-icon-search"),
        (32, "el-icon-info"),
    )
    name = models.CharField(max_length=150, verbose_name="标题")
    orders = models.IntegerField(verbose_name="显示顺序")
    is_show = models.BooleanField(verbose_name="是否上架", default=True)
    is_delete = models.BooleanField(verbose_name="逻辑删除", default=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="结束时间")
    # icon = models.IntegerField(verbose_name="icon图标", choices=ICON_CHOOSE, default=1)
    icon = models.CharField(verbose_name="icon图标", default="el-icon-info", max_length=100, null=True, blank=True)

    class Meta:
        # 设置当前模型在数据迁移的时候不要为它创建表
        abstract = True

    def __str__(self):
        return self.name

    # @property
    # def getIcon(self):
    #     return self.ICON_CHOOSE[self.icon]