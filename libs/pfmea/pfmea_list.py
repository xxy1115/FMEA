# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class PfmeaList(BaseApi):
    def my_pfmea_list(self, token, user_id, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProject/list",
            "json": {
                "from": 0,
                "pageSize": 12,
                "platform": "",
                "projectSerialNum": "",
                "searchKey": search_key,
                "sortColumn": "",
                "userId": user_id,
                "userRole": "5"  # 我的FMEA传5
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data["items"]

    def share_pfmea_list(self, token, user_id, search_key=""):
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-pfmea/pfmeaProject/selectShareProject",
            "params": {
                "from": 0,
                "pageSize": 12,
                "searchKey": search_key,
                "userId": user_id,
                "type": 0
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data["items"]

    def all_pfmea_list(self, token, product_type, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProject/list",
            "json": {
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [],
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
                "searchId": "",
                "searchKey": search_key,
                "serialNums": "",
                "sort": "",
                "sortColumn": "",
                "sortValue": "",
                "status": "",
                "statusTime": "",
                "type": "",
                "userRole": "100"  # 全部FMEA传100
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data["items"]

    def template_pfmea_list(self, token, user_id, product_type, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaTemplate/getAllTemplateList",
            "json": {
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [],
                "isUpProduct": "",
                "measureClassifyList": [],
                "pageSize": 15,
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
                "projectType": "pfmea",
                "searchId": "",
                "searchKey": search_key,
                "serialNums": [],
                "sort": "",
                "sortColumn": "",
                "sortValue": "",
                "status": "",
                "statusTime": "",
                "type": "",
                "userId": user_id
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data["items"]
