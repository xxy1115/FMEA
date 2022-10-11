# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getProcessFeature(BaseApi):
    def get_process_feature(self, token, product_type, search_key=""):
        """
        获取过程特性信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/processFeatureCategory/list",
            "json": {
                "depNames": "",
                "elementType": "clearAll",
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
        items = res.json()["data"]["items"]
        return items
