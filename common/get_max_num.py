# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getMaxNum(BaseApi):
    def get_max_num(self, token, searchTable, searchColumn, searchInitialLetter):
        """生成编号"""
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-system/genNum/getMaxNum",
            "params": {
                "searchTable": searchTable,
                "searchColumn": searchColumn,
                "searchInitialLetter": searchInitialLetter,
                "defaultNumTail": 1803090001
            }
        }
        res = self.send(data)
        max_num = json.loads(res.json()["data"])["maxNum"]
        return max_num
