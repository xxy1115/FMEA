# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_invalid import getInvalid
from common.get_measure_occ import getMeasureP
from common.get_product import getProduct


class bomList(BaseApi):
    def bom_list(self, token, product_type, search_key):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/list",
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
        result = res.json()["data"]["items"]
        return result
