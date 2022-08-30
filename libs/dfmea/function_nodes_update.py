# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_function import getFunction
from common.get_function_type import getFunctionType
from common.get_product import getProduct


class functionNodesUpdate(BaseApi):
    def add_function_nodes(self, data, token, product_type, ppt_serial):
        self.token = token
        for item in data["api"]["json"]:
            fun_name = item["functionName1"]
            res = getFunction().get_function(token, product_type, fun_name)  # 查询功能名称获取功能信息
            function_serial = res[0]["serialNum"]  # 获取要添加的功能serialNum
            en_function = res[0]["enFunction"]  # 获取要添加的功能英文描述
            r = getFunctionType().get_function_type(token, function_serial)
            function_type = r[0]["functionType"]
            item["enFunctionName"] = en_function
            item["functionSerial1"] = function_serial
            item["functionType"] = function_type
            item["pptSerial"] = ppt_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectFunctions"]

    def edit_function_nodes(self, data, token, product_type, project_serial, serial_num):
        self.token = token
        fun_name = data["api"]["json"]["functionName1"]
        res = getFunction().get_function(token, product_type, fun_name)  # 查询功能名称获取功能信息
        function_serial = res[0]["serialNum"]  # 获取要编辑的功能serialNum
        data["api"]["json"]["enFunctionName"] = res[0]["enFunction"]
        data["api"]["json"]["functionSerial1"] = function_serial
        data["api"]["json"]["projectSerial"] = project_serial
        data["api"]["json"]["serialNum"] = serial_num
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]

    def del_function_nodes(self, token, serial_num, fun_name, pif_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectFunction/delete",
            "json": {
                "functionName": fun_name,
                "pifSerial": pif_serial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
