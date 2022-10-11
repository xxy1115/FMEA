# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getElementFun(BaseApi):
    def get_element_fun(self, token, product_type, search_key=""):
        """
        获取要素功能列表
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/elementFunction/list",
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
        result = res.json()["data"]["items"]
        return result
