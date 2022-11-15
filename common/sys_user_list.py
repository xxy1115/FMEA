# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class sysUserList(BaseApi):
    def sys_user_list(self, token, product_type, search_key=""):
        """
        Dfmea部分共享用户列表
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/user/sysUserList",
            "json": {
                "depNames": "",
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [],
                "ids": "",
                "isUpProduct": "",
                "lessonSearchKey": "",
                "measureClassifyList": [],
                "pageSize": 5,
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
        result = json.loads(res.json()["data"])
        return result