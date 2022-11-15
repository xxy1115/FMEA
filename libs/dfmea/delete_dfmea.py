# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class deleteDfmea(BaseApi):
    def delete_dfmea(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/gateway/fmea-system/project/delete?projectSerialNum={serial_num}",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result

    def delete_template_dfmea(self, token, template_serial_num):
        self.token = token
        data = {
            "method": "delete",
            "url": f"/gateway/fmea-system/productTemplate/deleteTemplate/{template_serial_num}"
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result
