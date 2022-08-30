# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class saveFeature(BaseApi):
    def save_feature(self, token, product_types):
        """
        创建特性
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        en_feature = f'Feature{cur_time}'
        feature_explain = f'特性{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/productFeatureCategory/saveOrUpdate",
            "json": {
                "enFeature": en_feature,
                "featureExplain": feature_explain,
                "productCategory": [],
                "productTypes": product_types
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result["productFeatureCategory"]

    def add_feature(self, token, product_feature_category, pf_serial):
        """
        在结构树上添加一个特性
        :return:
        """
        self.token = token
        en_feature = product_feature_category["enFeature"]
        feature = product_feature_category["featureExplain"]
        serial_num = product_feature_category["serialNum"]
        data = {
            "method": "post",
            "url": "/fmea/projectFeature/saveFeatures",
            "json": [{
                "controlFeature": "1",
                "enFeature": en_feature,
                "feature": feature,
                "featureSymbolSerial": "",
                "pfSerial": pf_serial,
                "productFeatureSerial": serial_num,
                "programId": "",
                "serialNum": serial_num,
                "sort": 1,
                "technicalRequirements": ""
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectFeatureList"]
