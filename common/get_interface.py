# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getInterface(BaseApi):
    def get_interface(self, token, search_key=""):
        """
        获取界面功能
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/interfaceDescribe/list",
            "json": {
                "from": 0,
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
        interfaces = res.json()["data"]["items"]
        return interfaces
