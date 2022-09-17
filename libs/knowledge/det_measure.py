# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class detMeasure(BaseApi):
    def save_det_measure(self, token, applicableObject, reactionPlan,type, product_types):
        """
        创建探测措施
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        measure = f'探测措施{cur_time}'
        enMeasure = f'detMeasure{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/detMeasure/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "controlMethod": "控制方法",
                "det": "10",
                "enMeasure": enMeasure,
                "measure": measure,
                "operationRecordForm": "记录表单",
                "productTypes": product_types,
                "reactionPlan": reactionPlan,
                "sampleFrequency": "样本频率",
                "samplesize": "样本容量",
                "technicalrequirement": "标准要求",
                "type": type
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_det_measure(self, token, det_measure_serial):
        """
        从探测措施库删除指定serialNum的探测措施
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/detMeasure/delete",
            "data": det_measure_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
