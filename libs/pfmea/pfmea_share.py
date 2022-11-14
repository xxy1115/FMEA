# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class PfmeaShare(BaseApi):
    def pfmea_share_all(self, token, project_id, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProject/shareProject",
            "json": {
                "isShare": "2",  # 全部共享
                "projectId": project_id,
                "projectSerial": project_serial,
                "shareTime": "2050-11-29T16:00:00.000Z",
                "teamMember": [],
                "userMember": []
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data

    def pfmea_share_part(self, token, project_id, project_serial, user_id, user_name):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProject/shareProject",
            "json": {
                "isShare": "1",  # 部分共享
                "projectId": project_id,
                "projectSerial": project_serial,
                "teamMember": [],
                "userMember": [{
                    "member": user_id,
                    "projectId": project_id,
                    "shareTime": "",
                    "sharerId": f"{user_id}",
                    "userName": user_name
                }]
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data
