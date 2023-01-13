# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getAllPptSerial(BaseApi):
    def get_all_ppt_serial(self, token, project_serial):
        self.token = token
        data = {
            "method": "get",
            "url": f"/gateway/fmea-dfmea/project/getAllPptSerialByProjectSerial/{project_serial}"
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
        # dict_obj = {}  # 存储传入的字典key和对应的value
        # for key in dict:
        #     for item in data["dict_key"]:
        #         if key == item:
        #             dict_obj[key] = dict[key][0]["code"]
        # return dict_obj
