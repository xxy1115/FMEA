# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class procedureFunction(BaseApi):
    def save_procedure_fun(self, token, types, category, product_types):
        """
        创建工序功能
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        function = f'工序功能{cur_time}'
        enFunction = f'PF{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/procedureFunction/saveOrUpdate",
            "json": {
                "enFunction": enFunction,
                "function": function,
                "functionCategory": category,
                "functionType": types,
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

    def del_procedure_fun(self, token, pf_serial):
        """
        从工序功能库删除指定serialNum的工序功能
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/procedureFunction/delete",
            "data": pf_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
