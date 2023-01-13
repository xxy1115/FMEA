# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi


class selectUpProduct(BaseApi):
    def select_up_product(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/selectUpProduct",
            "data": project_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
