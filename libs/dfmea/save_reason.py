# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.select_function_product_type_by_serial import selectFunctionProductTypeBySerialNum


class saveReason(BaseApi):
    def save_reason(self, token, applicableObject, category, invalidUseType, product_types):
        """
        创建失效原因
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        invalidmode = f'失效原因{cur_time}'
        enInvalidMode = f'InvalidReason{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/invalidMode/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "category": category,
                "enInvalidMode": enInvalidMode,
                "failureClass": "",
                "invalidUseType": invalidUseType,
                "invalidmode": invalidmode,
                "occurrence": "10",
                "productCategory": [],
                "productTypes": product_types,
                "severity": "10"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        serial_num = res.json()["data"]["serialNum"]
        return [serial_num, invalidmode]

    def add_reason(self, token, serial_number, invalidmode, invalid_obj):
        """
        在结构树上添加一个失效原因
        :return:
        """
        self.token = token

        data = {
            "method": "post",
            "url": "/fmea/projectInvalid/saveOrUpdate",
            "json": [{
                "edituser": 2,
                "invalidmodeName": invalidmode,
                "invalidmodeSerial": serial_number,
                "occurrence": "10",
                "programId": "",
                "severity": "10"
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        project_invalids = result["projectInvalids"]
        # 获取失效网
        project_invalid_nets = self.save_invalid_nets(token, project_invalids[0]["serialNum"], invalidmode, invalid_obj)
        # 获取功能网
        save_pf_relation = self.save_pf_relation(token, invalid_obj["pfeSerial"])
        return [project_invalids, project_invalid_nets, save_pf_relation]

    def save_pf_relation(self, token, pfe_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/ktNew/forEachSaveGnjmjzPfRelation",
            "json": {
                "parentPfeSerial": pfe_serial,
                "pfSerials": [],
                "pfeSerials": []
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result

    def save_invalid_nets(self, token, serial_number, invalidmode, invalid_obj):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/saveProjectInvalidNets",
            "json": [{
                "det": "10",
                "edituser": "2",
                "firstPfSerial": invalid_obj["pfSerial"],
                "firstPidSerial": invalid_obj["serialNum"],
                "firstPifSerial": "",
                "firstPptSerial": invalid_obj["pptSerial"],
                "occurrence": "10",
                "pifSerial": "",
                "programId": "",
                "reasonName": invalidmode,
                "secondPidSerial": serial_number,
                "severity": "10",
                "type": "1"
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["projectInvalidNets"]
