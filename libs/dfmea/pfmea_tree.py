# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class PfmeaTree(BaseApi):
    def pfmea_tree(self, token, serial_num):
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-pfmea/pfmeaTree/getProjectProcedureByProjectSerialNum",
            "params": {"serialNum": serial_num}
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        pfmea_tree = res.json()["data"]
        return pfmea_tree["root"]
