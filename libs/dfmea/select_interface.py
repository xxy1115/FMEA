# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class selectInterface(BaseApi):
    def select_interface(self, token, if_type, search_key=""):
        """
        选择界面功能
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/interfaceDescribe/list",
            "json": {
                "from": 0,
                "interfaceDescribeType": if_type,
                "pageSize": 10,
                "procedureTypes": [],
                "productCategorys": [],
                "productTypes": [],
                "searchKey": search_key,
                "sort": "",
                "sortColumn": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        interface = res.json()["data"]["items"]
        return interface