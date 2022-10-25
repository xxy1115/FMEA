# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getDict(BaseApi):
    def get_dict(self, token):
        """
        获取字典
        :param token:
        :return: 返回所有字典key和value
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-system/dictionary/getDics"
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        dict = json.loads(res.json()["data"])
        return dict
        # dict_obj = {}  # 存储传入的字典key和对应的value
        # for key in dict:
        #     for item in data["dict_key"]:
        #         if key == item:
        #             dict_obj[key] = dict[key][0]["code"]
        # return dict_obj
