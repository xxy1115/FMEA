# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class selectFeatureProductTypeBySerialNum(BaseApi):
    def select_ft_p_t_by_serial(self, token, serial_num):
        self.token = token
        data = {
            "method": "get",
            "url": "/fmea/projectFeature/selectFeatureProductTypeBySerialNum",
            "params": {
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result
