# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getFunctionGroup(BaseApi):
    def get_function_group(self, token, product_type, search_key=""):
        """
        获取失效信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/main_data_end/functionGrouping/list",
            "json": {
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
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        items = res.json()["data"]["items"]
        return items
