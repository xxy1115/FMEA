# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_invalid import getInvalid


class invalidNodesUpdate(BaseApi):
    def add_invalid_nodes(self, data, token, product_type, ppt_serial, pf_serial):
        self.token = token
        for item in data["api"]["json"]:
            invalid_name = item["invalidmodeName"]
            res = getInvalid().get_invalid(token, product_type, invalid_name)  # 查询失效名称获取失效信息
            item["enInvalidModeName"] = res[0]["enInvalidMode"]
            item["invalidmodeSerial"] = res[0]["serialNum"]  # 获取要添加的失效serialNum
            item["occurrence"] = res[0]["occurrence"]
            item["severity"] = res[0]["severity"]
            item["pfSerial"] = pf_serial
            item["pptSerial"] = ppt_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectInvalids"]

    def edit_invalid_nodes(self, data, token, product_type, serial_num):
        self.token = token
        invalid_name = data["api"]["json"]["invalidmodeName"]
        res = getInvalid().get_invalid(token, product_type, invalid_name)  # 查询失效名称获取失效信息
        data["api"]["json"]["enInvalidModeName"] = res[0]["enInvalidMode"]
        data["api"]["json"]["invalidmodeSerial"] = res[0]["serialNum"]
        data["api"]["json"]["occurrence"] = res[0]["occurrence"]
        data["api"]["json"]["severity"] = res[0]["severity"]
        data["api"]["json"]["serialNum"] = serial_num
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]

    def del_invalid_nodes(self, token, invalid_name, pif_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectInvalid/delete",
            "json": {
                "pidName": invalid_name,
                "serialNum": serial_num
                # "pifSerial": pif_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
