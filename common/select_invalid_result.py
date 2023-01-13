# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class selectInvalidResultList(BaseApi):
    def select_invalid_reason_list_by_product(self, token, product_type, pf_serial, ppt_serial, search_key=""):
        """
        获取零件原因
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/invalidNet/selectProductInvalidResultList",
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
                "lessonSearchKey": "",
                "measureClassifyList": [],
                "pageSize": 10,
                "pfSerial": pf_serial,
                "pifSerial": "",
                "pptSerial": ppt_serial,
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": product_type,
                "programId": "",
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
        result = res.json()["data"]
        return result["items"]

    def select_invalid_result_list_by_inner_interface(self, token, product_type, pf_serial, ppt_serial, search_key=""):
        """
        获取界面原因
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/invalidNet/selectInvalidResultListByInterface",
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
                "lessonSearchKey": "",
                "measureClassifyList": [],
                "pageSize": 10,
                "pfSerial": pf_serial,
                "pifSerial": "",
                "pptSerial": ppt_serial,
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": product_type,
                "programId": "",
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
        result = res.json()["data"]
        return result["items"]
