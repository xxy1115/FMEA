# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_function import getFunction
from common.get_invalid import getInvalid


class Functions(BaseApi):
    def save_function(self, token, category, customers, types, product_types, standardId, standardNumAndName):
        """
        创建功能
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        en_function = f'Function{cur_time}'
        function = f'功能{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/function/saveOrUpdate",
            "json": {
                "category": category,
                "customers": customers,
                "enFunction": en_function,
                "function": function,
                "functionCategory": category,
                "functionTypes": types,
                "productTypes": product_types,
                "standardId": standardId,
                "standardNumAndName": standardNumAndName,
                "technicalRequirement": "标准要求"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return [result, function]

    def del_function(self, token, function_serial):
        """
        从功能库删除指定serialNum的功能
        :param token:
        :param function_serial:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/function/delete",
            "data": function_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def add_function_invalid(self, token, product_type, function_serial):
        """
        在产品功能库中添加失效
        :return:
        """
        self.token = token
        list = getInvalid().get_invalid(token, product_type)
        invalid_serial = list[0]["serialNum"]  # 获取要添加的失效serialNum
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/function/addFunctionInvalid",
            "json": [{
                "functionSerial": function_serial,
                "invalidSerial": invalid_serial,
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_function_invalid(self, token, product_type, function_name):
        """
        删除产品功能库的失效
        :return:
        """
        self.token = token
        list = getFunction().get_function(token, product_type, function_name)
        function_invalid_serial = list[0]["invalidList"][0]["functionInvalidSerial"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/function/deleteFunctionInvalid",
            "data": function_invalid_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
