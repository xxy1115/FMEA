# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class selectFunctionProductTypeBySerialNum(BaseApi):
    def select_f_p_t_by_serial(self, token, serial_num):
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-dfmea/projectFunction/selectFunctionProductTypeBySerialNum",
            "params": {
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
