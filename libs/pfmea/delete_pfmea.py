# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_max import getMax
from common.get_max_num import getMaxNum


class deletePFMEA(BaseApi):
    def delete_pfmea(self, token, project_serial):
        """
        删除PFMEA
        :param data:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProject/delete",
            "data": project_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
