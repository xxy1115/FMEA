# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class DfmeaTree(BaseApi):
    def dfmea_tree(self, token, serial_num):
        self.token = token
        data = {
            "method": "get",
            "url": "/fmea/dfmeaTree/getDfmeaTreeBySerialNum",
            "params": {"serialNum": serial_num}
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        dfmea_tree = json.loads(res.json()["data"])
        return dfmea_tree["root"]
