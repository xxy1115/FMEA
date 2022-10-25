# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class processProcedure(BaseApi):
    def save_process_procedure(self, token, procedureType, product_types):
        """
        创建过程工序
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        processProcedure = f'过程工序{cur_time}'
        enProcessProcedure = f'PP{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/processProcedure/saveOrUpdate",
            "json": {
                "enProcessProcedure": enProcessProcedure,
                "factoryCode": "工厂代码",
                "procedureType": procedureType,
                "processCode": "工序代码",
                "processNo": "",
                "processProcedure": processProcedure,
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

    def del_process_procedure(self, token, pp_serial):
        """
        从过程工序库删除指定serialNum的过程工序
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/processProcedure/delete",
            "data": pp_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
