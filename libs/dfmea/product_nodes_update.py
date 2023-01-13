# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_product import getProduct


class productNodesUpdate(BaseApi):
    def add_product_nodes(self, token, product_type, project_serial, product_serial, num):
        self.token = token
        res = getProduct().get_product(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/addProductNodes",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enProductName": res[i]["enProductName"], "level": 1, "parentSerial": product_serial,
                 "partsNum": res[i]["productNum"],
                 "partsName": res[i]["productName"], "productName": res[i]["productName"],
                 "productId": res[i]["productId"], "projectSerial": project_serial,
                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = res.json()["data"]
        return res_data

    def edit_product_nodes(self, token, product_type, serial_num):
        self.token = token
        res = getProduct().get_product(token, product_type)
        product = res[3]
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/updateProjectProductTree",
            "json": {
                "partsName": product["productName"],
                "productId": product["productId"],
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result["flag"]

    def del_product_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/delProductNodes",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
