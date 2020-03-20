from tablestore import *
from django.conf import settings


class TableStore(object):
    """tablestore工具类"""
    def __init__(self):
        self.client = OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def get_one(self, table_name, primary_key, columns_to_get=[]):
        """根据主键获取一天数据"""
        try:
            consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)
        except:
            return {}

        if return_row is None:
            return {}
        else:
            result = return_row.primary_key + return_row.attribute_columns
            print(result)
            data = {}
            for item in result:
                data[item[0]] = item[1]

            return data

    def add_one(self, table_name, primary_key, attribute_columns):
        """添加一条数据"""
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        try:
            # 调用put_row方法，如果没有指定ReturnType，则return_row为None
            consumed, return_row = self.client.put_row(table_name, condition)
        # 客户端异常，一般为参数错误或网络异常
        except OTSClientError as e:
            print(e.get_error_message())
            return False

        # 服务端异常，一般为参数错误或者流控错误
        except OTSServiceError as e:
            print(f"put row failed, "
                  f"http_status:{e.get_http_status()}, "
                  f"error_code:{e.get_error_code()}, "
                  f"error_message:{e.get_error_message()}, "
                  f"request_id:{e.get_request_id()}"
                  )
            return False
        return True

    def del_one(self, table_name, primary_key):
        """删除一条数据"""
        row = Row(primary_key)
        try:
            consumed, return_row = self.client.put_row(table_name, row, None)

        # 客户端异常，一般为参数错误或网络异常
        except OTSClientError as e:
            print(f"删除数据失败!, 状态码:{e.get_http_status()}, 错误信息:{e.get_error_message()}")
            return False

        # 服务端异常，一般为参数错误或者流控错误
        except OTSServiceError as e:
            print(f"put row failed, "
                  f"http_status:{e.get_http_status()}, "
                  f"error_code:{e.get_error_code()}, "
                  f"error_message:{e.get_error_message()}, "
                  f"request_id:{e.get_request_id()}"
                  )
            return False
        return True











