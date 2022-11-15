# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class DfmeaList(BaseApi):
    def dfmea_list(self, token, use_id, user_role, search_key=""):
        """我的Dfmea列表"""
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/project/list",
            "json": {
                "from": 0,
                "pageSize": 12,
                "platform": "",
                "projectSerialNum": "",
                "searchKey": search_key,
                "sortColumn": "",
                "userId": use_id,
                "userRole": user_role
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["items"]

    def share_dfmea_list(self, token, user_id, search_key=""):
        """共享Dfmea列表"""
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-system/project/selectShareProject",
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
        res_data = json.loads(res.json()["data"])
        return res_data["items"]

    def all_dfmea_list(self, token, product_type, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/project/list",
            "json": {
                "customer": "",
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
        res_data = json.loads(res.json()["data"])
        return res_data["items"]

    def template_dfmea_list(self, token, user_id, product_type, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/productTemplate/getAllTemplateList",
            "json": {
                "customer": "",
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [],
                "isUpProduct": "",
                "lessonSearchKey": "",
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
                "projectType": "dfmea",
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
        res_data = json.loads(res.json()["data"])
        return res_data["items"]
