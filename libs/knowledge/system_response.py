# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class systemResponse(BaseApi):
    def save_system_response(self, token, product_types):
        """
        创建系统响应措施
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        measure = f'诊断监视措施{cur_time}'
        enMeasure = f'diagnose{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/knowledgeSystemResponseMeasure/saveOrUpdate",
            "json": {
                "enMeasure": enMeasure,
                "measure": measure,
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

    def del_system_response(self, token, system_response_serial):
        """
        从删除指定serialNum的系统响应措施
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/knowledgeSystemResponseMeasure/delete",
            "data": system_response_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
