# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class elementFunction(BaseApi):
    def save_element_function(self, token, category, elementType, product_types):
        """
        创建要素功能
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        function = f'要素功能{cur_time}'
        enFunction = f'EF{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/elementFunction/saveOrUpdate",
            "json": {
                "enFunction": enFunction,
                "function": function,
                "functionCategory": category,
                "functionType": elementType,
                "productTypes": product_types
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_element_function(self, token, ef_serial):
        """
        从要素功能库删除指定serialNum的要素功能
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/elementFunction/delete",
            "data": ef_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
