# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_product import getProduct

class productNodesUpdate(BaseApi):
    def add_product_nodes(self, data, token, product_type, project_serial, product_serial):
        self.token = token
        for item in data["api"]["json"]:
            if len(item["partsName"]) > 0:  # 产品名称有数据时用产品名称查询，没有时用产品编号查询
                search_key = item["partsName"]
            elif len(item["partsNum"]) > 0:
                search_key = item["partsNum"]
            else:
                print("产品编号和名称至少输入一个")
            res = getProduct().get_product(token, product_type, search_key)  # 获取指定产品编号的产品信息
            product = res[0]
            item["partsNum"] = product["productNum"]
            item["partsName"] = product["productName"]
            item["productName"] = product["productName"]
            item["productId"] = product["productId"]
            item["enProductName"] = product["enProductName"]
            item["projectSerial"] = project_serial
            item["parentSerial"] = product_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data

    def edit_product_nodes(self, data, token, product_type, serial_num):
        self.token = token
        parts_name = data["api"]["json"]["partsName"]
        res = getProduct().get_product(token, product_type, parts_name)  # 获取指定产品名称的产品信息
        data["api"]["json"]["productId"] = res[0]["productId"]  # 取产品名称匹配的第一个产品ID
        data["api"]["json"]["serialNum"] = serial_num
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]

    def del_product_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/project/delProductNodes",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
