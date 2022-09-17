# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class diagnoseMonitor(BaseApi):
    def save_diagnose_monitor(self, token, product_types):
        """
        创建诊断监视措施
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        measure = f'诊断监视措施{cur_time}'
        enMeasure = f'diagnose{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/knowledgeDiagnoseMonitorMeasure/saveOrUpdate",
            "json": {
                "enMeasure": enMeasure,
                "measure": measure,
                "monitor": "5",
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

    def del_diagnose_monitor(self, token, diagnose_measure_serial):
        """
        从删除指定serialNum的诊断监视措施
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/knowledgeDiagnoseMonitorMeasure/delete",
            "data": diagnose_measure_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
