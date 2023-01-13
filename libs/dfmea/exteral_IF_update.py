# -*- coding: UTF-8 -*-
import json
import random

from common.base import BaseApi
from common.get_all_ppt_serial import getAllPptSerial
from common.get_product import getProduct
from libs.dfmea.select_interface import selectInterface


class exteralIFUpdate(BaseApi):
    def add_exteral_IF(self, token, if_type_list, product_type, project_serial, num):
        self.token = token
        IFs = selectInterface().select_interface(token, if_type_list[0]["code"])  # 查询界面分类为物理连接的界面功能
        if len(IFs) < 3:  # 查询结果小于3个，则查询全部界面功能
            IFs = selectInterface().select_interface(token, "")
        products = getProduct().get_product(token, product_type)  # 查询产品库作为外部产品
        res = getAllPptSerial().get_all_ppt_serial(token, project_serial)  # 获取内部产品
        in_products = res["list"][0]
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/ktNew/saveExteralInterfaceList",
            "json": []
        }
        for i in range(num):
            data["json"].append({
                "enInterfaceDescribe": IFs[i]["enInterfaceDescribe"],
                "enInternalProduct": in_products["enProductName"],
                "enKtNodeName1": products[i + 4]["enProductName"],
                "enMiddleNodeName": "jiezhi",
                "interfaceDescribe": IFs[i]["interfaceDescribe"],
                "interfaceDescribeSerial": IFs[i]["serialNum"],
                "interfaceType": 1,
                "ktNodeName1": products[i + 4]["productName"],
                "ktNodeName2": in_products["productName"],
                "ktNodeSerial1": "",
                "ktNodeSerial2": in_products["serialNum"],
                "lineType": 1,  # 界面类型(1-7)
                "middleNodeName": "介质",
                "middleNodeSerial": "",
                "projectSerial": project_serial
            })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_exteral_IF(self, token, pif_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/ktNew/deleteKtLineBySerial",
            "data": pif_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["meta"]["success"]
        return result
