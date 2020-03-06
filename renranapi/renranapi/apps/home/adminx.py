import xadmin
from .models import Banner

class BannerModelAdmin(object):
    list_display = ["id", "name", "link", "is_show", "start_time", "end_time"]
    list_editable = ["is_show", "start_time", "end_time"]

xadmin.site.register(Banner, BannerModelAdmin)