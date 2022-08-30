# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getFunctionType(BaseApi):
    def get_function_type(self, token, function_serial):
        """
        获取功能类型
        :param token:
        :param function_serial: 功能的serialNum
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/function/getFunctionTypeList",
            "data": function_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        function_types = res.json()["data"]["functionTypeList"]
        return function_types
