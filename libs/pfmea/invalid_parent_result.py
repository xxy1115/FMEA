# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_invalid import getInvalid
from common.get_procedure_function import getProcedureFun


class invalidParentResult(BaseApi):
    def findParentProcedureFailure(self, token, product_type, ppp_serial, search_key=""):
        """
        工序功能失效添加后果--上级失效列表
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/findParentProcedureFailure",
            "json": {
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionCategoryListQueryP": "",
                "functionTypes": [],
                "invalidUseType": [],
                "isUpProduct": "",
                "measureClassifyList": [],
                "pageSize": 10,
                "pfSerial": "",
                "pifSerial": "",
                "pppSerial": ppp_serial,
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": product_type,
                "programSerialNum": "",
                "projectSerial": "",
                "searchId": "",
                "searchKey": search_key,
                "serialNums": "",
                "sort": "",
                "sortColumn": "",
                "sortValue": "",
                "status": "",
                "statusTime": "",
                "type": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def saveFeatureMatrixRelation(self, token, pf_serial, parent_pf_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/processFlow/saveProcedureFeatureMatrixRelation",
            "json": {
                "procedureProductFeatureSerial": pf_serial,
                "productProductFeatureSerial": parent_pf_serial,
                "relation": "1"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def saveOrUpdate(self, token):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/saveOrUpdate",
            "json": []
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def saveInvalidNets(self, token, feature, en_feature, firstPfSerial, firstPidSerial, secondPfSerial,
                        secondPidSerial, secondPpSerial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaInvalidNet/saveInvalidNets",
            "json": [{
                "det": "10",
                "enFeature": en_feature,  # 父级功能
                "feature": feature,  # 父级功能
                "firstPfSerial": firstPfSerial,  # 父级功能
                "firstPfaSerial": "",
                "firstPidSerial": firstPidSerial,
                "firstPpSerial": "",
                "occurrence": "10",
                "secondPfSerial": secondPfSerial,
                "secondPfaSerial": "",
                "secondPidSerial": secondPidSerial,
                "secondPpSerial": secondPpSerial,
                "severity": "10"
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
