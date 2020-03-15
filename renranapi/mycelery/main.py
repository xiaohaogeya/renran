# 主程序
import os
from celery import Celery

# 创建celery实例对象
app = Celery("renran")

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'renranapi.settings.dev')
# 对django框架执行虚拟化
import django
django.setup()
# 通过app对象加载配置
app.config_from_object("mycelery.config")

# 自动搜索并加载任务
# 参数必须是一个列表,里面的每一个任务都是任务的路径名称
app.autodiscover_tasks(["mycelery.sms", "mycelery.article"])
