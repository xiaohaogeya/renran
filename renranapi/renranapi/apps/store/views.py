from django.shortcuts import render

# Create your views here.

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from tablestore import TableMeta, TableOptions, Condition, PutRowItem, BatchWriteRowRequest, \
    TableInBatchWriteRowItem, RowExistenceExpectation, Direction, INF_MIN, INF_MAX, \
    ReservedThroughput, CapacityUnit, OTSClient, PK_AUTO_INCR, Row
from datetime import datetime


class TableAPIView(APIView):
    @property
    def client(self):
        return OTSClient(
            settings.OTS_ENDPOINT,
            settings.OTS_ID,
            settings.OTS_SECRET,
            settings.OTS_INSTANCE
        )

    def post(self, request):
        """创建表"""
        # 设置主键和字段
        table_name = "user_message_table"

        # 主键列
        schema_of_primary_key = [
            ("user_id", "INTEGER"),
            ("sequence_id", "INTEGER", PK_AUTO_INCR),
            ("sender_id", "INTEGER"),
            ("message_id", "INTEGER")
        ]

        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)

        # 设置数据的有效期
        table_option = TableOptions(7 * 86400, 5)

        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0 ,0))

        # 创建数据
        self.client.create_table(table_meta, table_option, reserved_throughput)

        return Response({"message": "ok"})

    def delete(self, request):
        """删除表"""
        table = "user_message_table"
        self.client.delete_table(table)
        return Response({"message": "ok"})

    def get(self, request):
        """列出所有的表"""
        table_list = self.client.list_table()
        for table in table_list:
            print(table)

        return Response({"message": "ok"})


class DataAPIView(APIView):
    @property
    def client(self):
        return OTSClient(
            settings.OTS_ENDPOINT,
            settings.OTS_ID,
            settings.OTS_SECRET,
            settings.OTS_INSTANCE
        )

    def post(self, request):
        """添加数据到表格中"""
        table_name = "user_message_table"
        # 主键列
        primary_key = [
            # ("主键名", "值")
            ("user_id", 3),     # 接收Feed的用户ID
            ("sequence_id", PK_AUTO_INCR),  # 如果是自增主键，则值就是PK_AUTO_INCR
            ("sender_id", 1),   # 发布Feed的用户ID
            ("message_id", 4)   # 文章ID
        ]
        attribute_columns = [
            ("recervice_time", datetime.now().timestamp()),
            ("read_status", False)
        ]
        row = Row(primary_key, attribute_columns)
        consumed, return_row = self.client.put_row(table_name, row)
        print(return_row)

        return Response({"message": "ok"})

    def get(self, request):
        """获取指定数据"""
        table_name = "user_message_table"
        primary_key = [
            ("user_id", 3),
            ("sequence_id", 1234567890),
            ("sender_id", 1),
            ("message_id", 4)
        ]
        columns_to_get = []
        consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)
        print(return_row.attribute_columns)

        return Response({"message": "ok"})


class RowAPIView(APIView):
    @property
    def client(self):
        return OTSClient(
            settings.OTS_ENDPOINT,
            settings.OTS_ID,
            settings.OTS_SECRET,
            settings.OTS_INSTANCE
        )

    def get(self, request):
        """多行数据操作"""
        table_name = "user_message_table"

        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ("user_id", 3),
            ("sequence_id", INF_MIN),
            ("sender_id", INF_MIN),
            ("message_id", INF_MIN)
        ]
        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ("user_id", 3),
            ("sequence_id", INF_MAX),
            ("sender_id", INF_MAX),
            ("message_id", INF_MAX)
        ]

        # 查询所有列
        columns_to_get = []  # 表示返回所有列
        limit = 5

        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,
            Direction.FORWARD,
            inclusive_start_primary_key,
            exclusive_end_primary_key,
            columns_to_get,
            limit,
            max_version=1
        )
        print(f"一共返回了:{len(row_list)}")

        for row in row_list:
            print(row.primary_key, row.attribute_columns)

        return Response({"message": "ok"})

    def post(self, request):
        """添加多条数据"""
        table_name = "user_message_table"
        put_row_items = []

        for i in range(0, 10):
            # 主键列
            primary_key = [
                ("user_id", i),
                ("sequence_id", PK_AUTO_INCR),
                ("sender_id", 1),
                ("message_id", 4)
            ]

            attribute_columns = [
                ("recervice_time", datetime.now().timestamp()),
                ("read_status", False)
            ]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        print(result)

        return Response({"message": "ok"})
















