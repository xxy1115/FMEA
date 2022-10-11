# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getMeasurePfmea(BaseApi):
    def get_measure_occ(self, token, product_type, search_key=""):
        """
        获取预防措施信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/occMeasure/list",
            "json": {
                "applicableObject": "P",
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
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": product_type,
                "programSerialNum": "",
                "projectSerial": "",
                "pushRule": "1",
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
        product = res.json()["data"]["items"]
        return product

    def get_measure_det(self, token, product_type, search_key=""):
        """
        获取探测措施信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/detMeasure/list",
            "json": {
                "applicableObject": "P",
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
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": product_type,
                "programSerialNum": "",
                "projectSerial": "",
                "pushRule": "1",
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
        product = res.json()["data"]["items"]
        return product
