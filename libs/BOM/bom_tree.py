# -*- coding: UTF-8 -*-
import random

from common.base import BaseApi
from common.get_product import getProduct


class bomTree(BaseApi):
    def add_bom_products(self, token, product_type, bom_serial, parent_serial):
        """
        产品树添加下级产品
        :param token:
        :param serial_num:
        :return:
        """
        self.token = token
        products = getProduct().get_product(token, product_type)
        product = products[4]  # 取产品库中第5个产品
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/addBomProducts",
            "json": {
                "bomSerial": bom_serial,
                "parentSerial": parent_serial,
                "productId": product["productId"],
                "productName": product["productName"]
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
