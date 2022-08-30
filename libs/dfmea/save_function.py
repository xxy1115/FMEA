# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class saveFunction(BaseApi):
    def save_function(self, token, types, category, product_types):
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
            "url": "/knowledge_end/function/saveOrUpdate",
            "json": {
                "enFunction": en_function,
                "function": function,
                "functionCategory": category,
                "functionNum": "",
                "functionTypes": types,
                "productCategory": [],
                "productTypes": product_types
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return [result, en_function, function]

    def add_function(self, token, en_function, function, serial_num, ppt_serial):
        """
        在结构树上添加一个功能
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectFunction/saveOrUpdate",
            "json": [{
                "edituser": 1,
                "enFunctionName": en_function,
                "functionName1": function,
                "functionSerial1": serial_num,
                "functionType": "",
                "level": 1,
                "parentSerial": -1,
                "pptSerial": ppt_serial,
                "programId": ""
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectFunctions"]
