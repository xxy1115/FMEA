# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class programList(BaseApi):
    def program_list(self, token, product_type, search_key=""):
        """
        项目列表查询
        :param product_type: 产品类别权限列表
        :param search_key: 搜索关键字，不传查询全部项目
        :return: 查询结果列表
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-program/program/list",
            "json": {
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [ ],
                "isUpProduct": "",
                "measureClassifyList": [ ],
                "pfSerial": "",
                "pifSerial": "",
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [ ],
                "productId": "",
                "productIds": [ ],
                "productTypeList": product_type,
                "productTypes": product_type,
                "projectSerial": "",
                "searchId": "",
                "searchKey": search_key,
                "pageSize": 15,
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
        search_result = res.json()["data"]["items"]
        return search_result
