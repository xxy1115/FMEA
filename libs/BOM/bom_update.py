# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_invalid import getInvalid
from common.get_measure_occ import getMeasureP
from common.get_product import getProduct


class bomUpdate(BaseApi):
    def save_bom(self, token, bom_type, product_type):
        self.token = token
        max_num = self.get_max_num(token)  # 获取bom编号
        products = getProduct().get_product(token, product_type)
        product = products[2]  # 取产品库中第3个产品
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/save",
            "json": {
                "bomNum": max_num,
                "bomType": bom_type,
                "description": f"{max_num}BOM描述",
                "productId": product["productId"],
                "productName": product["productName"],
                "remark": f"{max_num}备注"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def get_max_num(self, token):
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-maindata/bom/getMaxNum",
            "params": {
                "searchTable": "bom",
                "searchColumn": "bom_num",
                "searchInitialLetter": "PB",
                "defaultNumTail": 1803090001
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]["maxNum"]
        return result

    def delete_bom(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/deleteBom",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
