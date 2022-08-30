# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getProduct(BaseApi):
    def get_product(self, token, product_type, search_key=""):
        """
        获取产品信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/main_data_end/product/list",
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
        product = res.json()["data"]["items"]
        return product
