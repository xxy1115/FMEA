# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi


class crChangeStatus(BaseApi):
    def cr_change_status1(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/saveOrUpdateCustomerRequestChangeStatus",
            "json": {
                "changeStatus": "1",
                "projectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def cr_change_status(self, token, user_id, project_serial, change_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/saveOrUpdateCustomerRequestChangeStatus",
            "json": {
                "changeStatus": "0",
                "createTime": "2022-10-19 14:51:51",
                "creator": user_id,
                "delFlg": "0",
                "projectSerial": project_serial,
                "serialNum": change_serial,
                "updateTime": "2022-10-19 14:51:51",
                "updater": user_id,
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
