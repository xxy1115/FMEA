# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_invalid import getInvalid
from common.get_procedure_function import getProcedureFun


class invalidReason(BaseApi):
    def selectInvalidReasonList(self, token, ppp_serial):
        """
        工序功能失效添加原因--原因列表
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-pfmea/pfmeaInvalidNet/selectInvalidReasonList",
            "params": {
                "serialNums": "",
                "pppSerial": ppp_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def findPreProcedureFailure(self, token, product_type, ppp_serial, search_key=""):
        """
        工序功能失效添加原因--上工序原因列表
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/findPreProcedureFailure",
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

    def saveFeatureMatrixRelation(self, token, ef_serial, pf_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/processFlow/saveFeatureMatrixRelation",
            "json": {
                "procedureProcessFeatureSerial": ef_serial,
                "procedureProductFeatureSerial": pf_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def saveInvalidNets(self, token, firstPfSerial, firstPidSerial, firstPpSerial, secondPeSerial, secondPfSerial,
                        secondPidSerial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaInvalidNet/saveInvalidNets",
            "json": [{
                "det": "10",
                "firstPeSerial": "",
                "firstPfSerial": firstPfSerial,
                "firstPfaSerial": "",
                "firstPidSerial": firstPidSerial,
                "firstPpSerial": firstPpSerial,
                "occurrence": "10",
                "secondPeSerial": secondPeSerial,
                "secondPfSerial": secondPfSerial,
                "secondPfaSerial": "",
                "secondPidSerial": secondPidSerial,
                "secondPpSerial": "",
                "severity": ""
            }]
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

    def saveFailureRelation(self, token, preProcedureFailureSerial, preProcedureSerial, procedureFailureSerial, procedureSerial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/saveFailureRelation",
            "json": [{
                "preProcedureFailureSerial": preProcedureFailureSerial,
                "preProcedureSerial": preProcedureSerial,
                "procedureFailureSerial": procedureFailureSerial,
                "procedureSerial": procedureSerial
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result