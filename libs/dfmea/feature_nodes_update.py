# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_feature import getFeature


class featureNodesUpdate(BaseApi):
    def add_feature_nodes(self, data, token, product_type, ppt_serial):
        self.token = token
        for item in data["api"]["json"]:
            search_key = item["feature"]
            res = getFeature().get_feature(token, product_type, search_key)  # 查询特性名称获取特性信息
            if len(res) > 0:
                item["enFeature"] = res[0]["enFeature"]  # 获取要添加的特性英文描述
                item["productFeatureSerial"] = res[0]["serialNum"]  # 获取要添加的特性serialNum
            elif len(res) <= 0:
                print("查询的特性不存在")
                return False
            item["pptSerial"] = ppt_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectFeatureList"]

    def edit_feature_nodes(self, data, token, product_type, serial_num):
        self.token = token
        search_key = data["api"]["json"]["feature"]
        res = getFeature().get_feature(token, product_type, search_key)  # 查询功能名称获取功能信息
        if len(res) > 0:
            data["api"]["json"]["productFeatureSerial"] = res[0]["serialNum"]  # 获取要添加的特性serialNum
        elif len(res) <= 0:
            print("查询的特性不存在")
            return False
        data["api"]["json"]["serialNum"] = serial_num
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]

    def del_feature_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectFeature/deleteFeature",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]
