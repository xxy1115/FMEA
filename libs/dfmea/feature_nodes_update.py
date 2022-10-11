# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_feature import getFeature


class featureNodesUpdate(BaseApi):
    def add_feature_nodes(self, token, product_type, ppt_serial, num):
        self.token = token
        res = getFeature().get_feature(token, product_type)
        data = {
            "method": "post",
            "url": "/fmea/projectFeature/saveFeatures",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"controlFeature": 1, "enFeature": res[i]["enFeature"], "feature": res[i]["featureExplain"],
                 "featureSymbolSerial": "", "pptSerial": ppt_serial, "productFeatureSerial": res[i]["serialNum"],
                 "programId": "", "serialNum": res[i]["serialNum"], "sort": i + 4,
                 "technicalRequirements": f"技术要求{i + 1}"
                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectFeatureList"]

    def edit_feature_nodes(self, token, product_type, serial_num):
        self.token = token
        res = getFeature().get_feature(token, product_type)
        feature = res[3]
        data = {
            "method": "post",
            "url": "/fmea/projectFeature/updateProjectFeature",
            "json": {
                "enTechnicalRequirements": "",
                "feature": feature["featureExplain"],
                "featureSymbolSerial": "",
                "productFeatureSerial": feature["serialNum"],
                "serialNum": serial_num,
                "technicalRequirements": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]
        #
        # search_key = data["api"]["json"]["feature"]
        # res = getFeature().get_feature(token, product_type, search_key)  # 查询功能名称获取功能信息
        # if len(res) > 0:
        #     data["api"]["json"]["productFeatureSerial"] = res[0]["serialNum"]  # 获取要添加的特性serialNum
        # elif len(res) <= 0:
        #     print("查询的特性不存在")
        #     return False
        # data["api"]["json"]["serialNum"] = serial_num
        # res = self.send(data["api"])
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
