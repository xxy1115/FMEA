# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_measure_pfmea import getMeasurePfmea


class measurePNodesUpdate(BaseApi):
    def add_measure_occ(self, token, product_type, ei_serial, num):
        self.token = token
        res = getMeasurePfmea().get_measure_occ(token, product_type)
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/saveProjectMeasures",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"det": res[i]["det"], "enMeasuresName": res[i]["enMeasure"], "measuresFrom": "0",
                 "measuresName": res[i]["measure"], "measuresSerial": res[i]["serialNum"], "measuresType": 0,
                 "occurrence": res[i]["occurrence"], "pidSerial": ei_serial,
                 "technicalrequirement": res[i]["technicalrequirement"]})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_measure_occ(self, token, product_type, serial_num, pidSerial, projectSerial):
        self.token = token
        res = getMeasurePfmea().get_measure_occ(token, product_type)
        enMeasuresName = res[3]["enMeasure"]
        measuresName = res[3]["measure"]
        measureSerial = res[3]["serialNum"]
        occurrence = res[3]["occurrence"]
        technicalrequirement = res[3]["technicalrequirement"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/updatePMOne",
            "json": [{
                "enMeasuresName": enMeasuresName,
                "measureSerial": measureSerial,
                "measuresName": measuresName,
                "measuresType": "0",
                "occurrence": occurrence,
                "pidSerial": pidSerial,
                "projectSerial": projectSerial,
                "serialNum": serial_num,
                "sync": False,
                "technicalrequirement": technicalrequirement
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_measure_occ(self, token, invalidMode, ppp_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/delete",
            "json": {
                "invalidMode": invalidMode,
                "invalidType": "FC",
                "measuresFrom": 0,
                "pppSerial": ppp_serial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def add_measure_det(self, token, product_type, ei_serial, num):
        self.token = token
        res = getMeasurePfmea().get_measure_det(token, product_type)
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/saveProjectMeasures",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"controlMethod": res[i]["controlMethod"], "det": res[i]["det"], "enMeasuresName": res[i]["enMeasure"],
                 "measuresFrom": "0",
                 "measuresName": res[i]["measure"], "measuresSerial": res[i]["serialNum"], "measuresType": 1,
                 "operationRecordForm": res[i]["operationRecordForm"], "pidSerial": ei_serial,
                 "reactionPlan": res[i]["reactionPlan"], "sampleFrequency": res[i]["sampleFrequency"],
                 "samplesize": res[i]["samplesize"], "technicalrequirement": res[i]["technicalrequirement"]})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_measure_det(self, token, product_type, serial_num, pidSerial, projectSerial):
        self.token = token
        res = getMeasurePfmea().get_measure_det(token, product_type)
        controlMethod = res[3]["controlMethod"]
        det = res[3]["det"]
        enMeasuresName = res[3]["enMeasure"]
        measuresName = res[3]["measure"]
        measureSerial = res[3]["serialNum"]
        operationRecordForm = res[3]["operationRecordForm"]
        reactionPlan = res[3]["reactionPlan"]
        sampleFrequency = res[3]["sampleFrequency"]
        samplesize = res[3]["samplesize"]
        technicalrequirement = res[3]["technicalrequirement"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/updatePMOne",
            "json": [{
                "controlMethod": controlMethod,
                "det": det,
                "enMeasuresName": enMeasuresName,
                "measureSerial": measureSerial,
                "measuresName": measuresName,
                "measuresType": "1",
                "operationRecordForm": operationRecordForm,
                "pidSerial": pidSerial,
                "projectSerial": projectSerial,
                "reactionPlan": reactionPlan,
                "sampleFrequency": sampleFrequency,
                "samplesize": samplesize,
                "serialNum": serial_num,
                "sync": False,
                "technicalrequirement": technicalrequirement
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_measure_det(self, token, invalidMode, ppp_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectMeasure/delete",
            "json": {
                "invalidMode": invalidMode,
                "invalidType": "FC",
                "measuresFrom": 0,
                "pppSerial": ppp_serial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
