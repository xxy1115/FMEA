# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi


class crPublish(BaseApi):
    def cr_publish(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/project/publishCR",
            "data": project_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result
