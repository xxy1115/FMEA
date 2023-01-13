# -*- coding: UTF-8 -*-
import json
import random

from common.base import BaseApi
from common.get_function import getFunction
from common.get_function_type import getFunctionType
from common.get_product import getProduct


class crFunctionUpdate(BaseApi):
    def add_cr_function(self, token, product_type, ppt_serial, num):
        self.token = token
        res = getFunction().get_function(token, product_type)  # 查询功能
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/projectFunction/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            function_serial = res[i]["serialNum"]
            funTypeList = getFunctionType().get_function_type(token, function_serial)
            # 生成32位随机数
            num = []
            for n in range(32):
                num.append(random.choice("1234567890abcdef"))
            cr_id = "".join(num)
            data["json"].append(
                {"crId": cr_id, "enFunctionName": res[i]["enFunction"], "functionName1": res[i]["function"],
                 "functionSerial1": res[i]["serialNum"], "functionType": funTypeList[0]["functionType"], "level": "1",
                 "parentSerial": "-1", "pptSerial": ppt_serial})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_cr_function(self, token, serial_num, fun_name, pif_serial):
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
