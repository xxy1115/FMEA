# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class batchInvalidNetUpdate(BaseApi):
    # 仅支持一对失效关联
    def batch_invalid_add(self, token, first, second):
        self.token = token
        first_PfSerial = first["pfSerial"]
        first_PidSerial = first["serialNum"]
        first_PptSerial = first["pptSerial"]
        severity = first["severity"]
        second_PfSerial = second["pfSerial"]
        second_PidSerial = second["serialNum"]
        second_PptSerial = second["pptSerial"]  # currentSerial和nextSerial传同样值
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/saveBatchInvalidNet",
            "json": [{
                "currentSerial": second_PptSerial,
                "firstPfSerial": first_PfSerial,
                "firstPidSerial": first_PidSerial,
                "firstPptSerial": first_PptSerial,
                "nextSerial": second_PptSerial,
                "secondPfSerial": second_PfSerial,
                "secondPidSerial": second_PidSerial,
                "secondPptSerial": second_PptSerial,
                "serialNum": "1",
                "severity": severity
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["flag"]

    def batch_invalid_del(self, token, first_PidSerial, second_PidSerial):
        self.token = token
        url = f'/fmea/invalidNet/deleteConsequncesByFirstPidSerialAndSecondPidSerial/{first_PidSerial}/{second_PidSerial}'
        data = {
            "method": "get",
            "url": url
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        return res_data["flag"]
