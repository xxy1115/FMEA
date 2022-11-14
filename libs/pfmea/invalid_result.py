# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_invalid import getInvalid
from common.get_procedure_function import getProcedureFun


class invalidResult(BaseApi):
    def findNextProcedureFailure(self, token, product_type, ppp_serial, search_key=""):
        """
        工序功能失效添加后果--后工序失效列表
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/findNextProcedureFailure",
            "json": {
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
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

    def saveFailureRelation(self, token, preProcedureFailureSerial, preProcedureSerial, procedureFailureSerial,
                            procedureSerial):
        """
        工序功能失效添加后果--选择后工序失效保存
        """
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
