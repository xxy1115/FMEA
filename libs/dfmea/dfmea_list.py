# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class DfmeaList(BaseApi):
    def dfmea_list(self, token, use_id, user_role, search_key=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/project/list",
            "json": {
                "from": 0,
                "pageSize": 12,
                "platform": "",
                "projectSerialNum": "",
                "searchKey": search_key,
                "sortColumn": "",
                "userId": use_id,
                "userRole": user_role
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["items"]
