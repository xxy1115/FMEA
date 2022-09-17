# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getProcessType(BaseApi):
    def get_process_type(self, token):
        """
        获取工序分类
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/fmea/processTypeIcon/getList"
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        list = json.loads(res.json()["data"])["list"]
        return list
