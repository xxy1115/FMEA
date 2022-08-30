# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class selectProductByPptSerial(BaseApi):
    def select_product_by_pptSerial(self, token, ppt_serial):
        self.token = token
        data = {
            "method": "get",
            "url": "/main_data_end/product/selectProductByPptSerial",
            "params": {
                "pptSerial": ppt_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        product = res.json()["data"]["product"]
        return product
