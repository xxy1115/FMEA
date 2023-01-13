# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_product import getProduct


class crProductUpdate(BaseApi):
    def add_cr_product(self, token, product_type, project_serial):
        self.token = token
        res = getProduct().get_product(token, product_type)
        product_Id = res[3]["productId"]  # 取产品库中第4个产品
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/saveCRUpProduct",
            "json": {
                "parentSerial": "0",
                "projectSerial": project_serial,
                "upProducts": [{"productId": product_Id}]
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = res.json()["data"]
        return res_data

    def del_cr_product(self, token, ppt_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/delCrTree",
            "data": ppt_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
