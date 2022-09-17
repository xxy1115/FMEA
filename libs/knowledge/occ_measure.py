# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class occMeasure(BaseApi):
    def save_occ_measure(self, token, applicableObject, pre_measure_type, product_types):
        """
        创建预防措施
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        measure = f'预防措施{cur_time}'
        enMeasure = f'preMeasure{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/occMeasure/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "enMeasure": enMeasure,
                "measure": measure,
                "measureType": "0",
                "occurrence": "10",
                "productCategory": [],
                "productTypes": product_types,
                "technicalrequirement": "标准要求",
                "type": pre_measure_type
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_occ_measure(self, token, occ_measure_serial):
        """
        从预防措施库删除指定serialNum的预防措施
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/occMeasure/delete",
            "data": occ_measure_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
