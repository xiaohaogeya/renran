# celery的任务必须写在tasks.py的文件中，别的文件名称不识别
from mycelery.main import app
from .yuntongxun.sms import CCP
from . import constants
import logging
log = logging.getLogger("django")
@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    """
    异步发送短信
    :param mobile:  手机号码
    :param sms_code:
    :return:
    """
    ccp = CCP()
    try:
        result = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
        return result
    except:
        log.error(f"发送短信验证码失败!手机号:{mobile}")
