# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getMeasureD(BaseApi):
    def get_measure_d(self, token, product_type, search_key=""):
        """
        获取探测措施信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/detMeasure/list",
            "json": {
                "applicableObject": "D",
                "customers": [],
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
        product = res.json()["data"]["items"]
        return product
