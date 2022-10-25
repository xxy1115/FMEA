# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class saveMeasure(BaseApi):
    def save_det_measure(self, token, applicableObject, measure_type, product_types):
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
            "url": "/gateway/fmea-knowledge/detMeasure/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "det": "10",
                "enMeasure": enMeasure,
                "measure": measure,
                "occurrence": "10",
                "productCategory": [],
                "productTypes": product_types,
                "type": measure_type
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        serial_num = res.json()["data"]["serialNum"]
        return [serial_num, measure, enMeasure]

    def add_det_measure(self, token, measure_serial, measure, enMeasure, invalid_serial):
        """
        在结构树上添加一个探测措施
        :return:
        """
        self.token = token

        data = {
            "method": "post",
            "url": "/gateway/fmea-system/projectMeasure/savePM",
            "json": [{
                "det": "10",
                "edituser": 1,
                "enMeasuresName": enMeasure,
                "measuresName": measure,
                "measuresSerial": measure_serial,
                "measuresType": "1",
                "pidSerial": invalid_serial,
                "programId": "",
                "sync": False
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return json.loads(res_data["projectMeasures"])

    def save_pre_measure(self, token, applicableObject, pre_measure_type, product_types):
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
            "url": "/gateway/fmea-knowledge/occMeasure/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "det": "10",
                "enMeasure": enMeasure,
                "measure": measure,
                "occurrence": "10",
                "productCategory": [],
                "productTypes": product_types,
                "type": pre_measure_type
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        serial_num = res.json()["data"]["serialNum"]
        return [serial_num, measure, enMeasure]

    def add_pre_measure(self, token, measure_serial, measure, enMeasure, pid_serial,pif_serial):
        """
        在结构树上添加一个预防措施
        :return:
        """
        self.token = token

        data = {
            "method": "post",
            "url": "/gateway/fmea-system/projectMeasure/savePM",
            "json": [{
                "edituser": 1,
                "enMeasuresName": enMeasure,
                "measuresName": measure,
                "measuresSerial": measure_serial,
                "measuresType": "0",
                "occurrence": "10",
                "pidSerial": pid_serial,
                "pifSerial": pif_serial,
                "programId": "",
                "sync": False
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["projectMeasures"]
