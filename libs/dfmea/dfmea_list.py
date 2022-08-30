# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class DfmeaList(BaseApi):
    def dfmea_list(self, data, token, use_id, user_role, search_key=""):
        self.token = token
        data["api"]["json"]["userId"] = use_id
        data["api"]["json"]["userRole"] = user_role
        data["api"]["json"]["searchKey"] = search_key
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["items"]
