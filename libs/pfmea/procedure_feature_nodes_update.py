# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_feature import getFeature
from common.get_procedure_function import getProcedureFun


class procedureFeatureNodesUpdate(BaseApi):
    def add_procedure_feature(self, token, product_type, serial_num, product_id, num):
        """
        添加产品特性--从产品特性库选择多个产品特性
        :param num: 添加产品特性的个数-3
        """
        self.token = token
        res = getFeature().get_pfmea_feature(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectFeature/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enFeature": res[i]["enFeature"], "feature": res[i]["featureExplain"],
                 "featureSymbolSerial": res[i]["productFeatureSymbol"],
                 "productFeatureSerial": res[i]["serialNum"],
                 "productProductFeature": {"featureSymbol": res[i]["productFeatureSymbol"],
                                           "productFeature": res[i]["featureExplain"],
                                           "productFeatureSerial": res[i]["serialNum"], "productId": product_id},
                 "projectFunctionSerial": serial_num, "projectProcedureSerial": serial_num,
                 "technicalRequirements": ""})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_procedure_feature(self, token, product_type, serial_num):
        """编辑产品特性--从产品特性列表选择第4个产品特性"""
        self.token = token
        res = getFeature().get_pfmea_feature(token, product_type)
        enFeature = res[3]["enFeature"]
        feature = res[3]["featureExplain"]
        productFeatureSerial = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectFeature/updateProjectFeature",
            "json": {
                "dfmeaPptSerial": "",
                "enFeature": enFeature,
                "feature": feature,
                "featureSymbol": "",
                "featureSymbolSerial": "",
                "pfmeaProductFeatureSerial": "",
                "productFeatureSerial": productFeatureSerial,
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

    def del_procedure_feature(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/gateway/fmea-pfmea/pfmeaProjectFeature/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
