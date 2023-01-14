# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class importFeature(BaseApi):
    def dfmeaFeatureList(self, token, product_type, product_id, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/kcds/selectAllDfmeaProductFeatureList",
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
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": product_id,
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
                "statusTime": "",
                "type": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result["items"]

    def dfmeaFeatureProductIdList(self, token, product_type, product_id, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/kcds/selectProductFeatureByProductId",
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
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": product_id,
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
                "statusTime": "",
                "type": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result["items"]

    def saveImportFeature(self, token, pfmea_project_serial, ppt_serial, product_id, features):
        self.token = token
        new_feature = []
        original_feature = []
        for index, item in enumerate(features):
            new_feature.append({
                "enFeature": item["enFeature"],
                "featureSymbol": item["featureSymbol"],
                "number": index + 1,
                "pfeSerial": item["serialNum"],
                "pfmeaProjectSerial": pfmea_project_serial,
                "pptSerial": ppt_serial,
                "productFeature": item["feature"],
                "productFeatureSerial": item["productFeatureSerial"],
                "productId": product_id,
                "source": "DFMEA",
                "sourceName": "DFMEA",
                "technicalRequirements": "技术要求"
            })
            original_feature.append({
                "enFeature": item["enFeature"],
                "featureSymbol": item["featureSymbol"],
                "number": index + 1,
                "pfmeaProjectSerial": pfmea_project_serial,
                "pptSerial": ppt_serial,
                "productFeature": item["feature"],
                "productFeatureSerial": item["productFeatureSerial"],
                "technicalRequirements": "技术要求"
            })
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/saveOrUpdate",
            "json": {
                "newPfmeaProductFeature": new_feature,
                "originalPfmeaProductFeature": original_feature
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def selectPfmeaProductFeatureList(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/selectPfmeaProductFeatureList",
            "json": {
                "currentPage": 1,
                "pageSize": 10,
                "projectSerial": project_serial,
                "versionPid": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def archiveProductFeature(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/archiveProductFeature",
            "json": {
                "projectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def getProductFeatureVersionList(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/getProductFeatureVersionList",
            "json": {
                "projectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def import_excel(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/importData",
            "files": {"excelFile": ("pfmea_feature.xls", open("pfmea_feature.xls", "rb"), "application/vnd.ms-excel")},
            "data": {
                "pfmeaProjectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
