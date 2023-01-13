# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_max_num import getMaxNum
from common.get_product import getProduct


class saveProduct(BaseApi):
    def save_product(self, token, product_level, product_types):
        """
        新建产品
        :param token:
        :return: [serialNum, 产品编号, 产品类别数组]
        """
        self.token = token
        max_num = getMaxNum().get_max_num(token, "product", "product_num", "PA")  # 获取产品编号
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/product/saveProduct",
            "json": {
                "enProductName": f'Product{max_num}',
                "productCategory": [],
                "productLevel": product_level,
                "productName": f'产品{max_num}',
                "productNum": max_num,
                "productType": "",
                "productTypes": product_types,
                "remark": f'备注{max_num}'
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        flag = res.json()["data"]["flag"]
        return [flag, max_num]

    def del_product(self, token, product_serial):
        """从知识库删除创建的产品"""
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/product/deleteProduct",
            "data": product_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def add_product(self, token, product_type, ppt_serial, project_serial, product_num):
        """
        在结构树上添加一个产品
        :param token:
        :param max_num:产品编号
        :return:
        """
        self.token = token
        res = getProduct().get_product(token, product_type, product_num)  # 获取指定产品编号的产品信息
        product_name = res[0]["productName"]
        product_id = res[0]["productId"]
        en_product_name = res[0]["enProductName"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/addProductNodes",
            "json": [{
                "enProductName": en_product_name,
                "level": 1,
                "parentSerial": ppt_serial,
                "partsName": product_name,
                "partsNum": product_num,
                "productId": product_id,
                "productName": product_name,
                "projectSerial": project_serial
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = res.json()["data"]
        return res_data
