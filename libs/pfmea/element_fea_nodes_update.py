# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_process_feature import getProcessFeature


class elementFeaNodesUpdate(BaseApi):
    def add_element_fea_nodes(self, token, product_type, pe_serial, num):
        """
        添加过程特性--从过程特性库选择多个过程特性
        :param num: 添加过程特性的个数-3
        """
        self.token = token
        res = getProcessFeature().get_process_feature(token, product_type)
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectFeature/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enFeature": res[i]["enFeature"], "feature": res[i]["featureExplain"], "featureSymbolSerial": "", "processFeatureSerial": res[i]["serialNum"],
                 "productProductFeature": {}, "projectElementSerial": "", "projectRealElementSerial": pe_serial})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_element_fea_nodes(self, token, product_type, serial_num):
        """编辑过程特性--从要过程特性列表选择第4个过程特性"""
        self.token = token
        res = getProcessFeature().get_process_feature(token, product_type)
        enFeature = res[3]["enFeature"]
        feature = res[3]["featureExplain"]
        featureSymbol = res[3]["featureSymbol"]
        processFeatureSerial = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectFeature/updateProjectFeature",
            "json": {
                "enFeature": enFeature,
                "feature": feature,
                "featureSymbol": featureSymbol,
                "featureSymbolSerial": "",
                "processFeatureSerial": processFeatureSerial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_element_fea_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/pfmea_end/pfmeaProjectFeature/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
