# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.select_function_product_type_by_serial import selectFunctionProductTypeBySerialNum


class saveInvalid(BaseApi):
    def save_invalid(self, token, applicableObject, category, failureClass, faultModeName, functionGroupId,
                     invalidUseType, product_types):
        """
        创建失效
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        invalidmode = f'失效{cur_time}'
        enInvalidMode = f'InvalidMode{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/invalidMode/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "category": category,
                "enInvalidMode": enInvalidMode,
                "failureClass": failureClass,
                "faultModeName": faultModeName,
                "functionGroupId": functionGroupId,
                "invalidUseType": invalidUseType,
                "invalidmode": invalidmode,
                "invalidmodeNum": "",
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
        return [serial_num, invalidmode, enInvalidMode]

    def add_invalid(self, token, invalid_serial, invalidmode, enInvalidMode, pfe_serial, ppt_serial):
        """
        在结构树上添加一个失效
        :return:
        """
        self.token = token

        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/projectInvalid/saveOrUpdate",
            "json": [{
                "edituser": 1,
                "enInvalidModeName": enInvalidMode,
                "invalidmodeName": invalidmode,
                "invalidmodeSerial": invalid_serial,
                "occurrence": "10",
                "pfeSerial": pfe_serial,
                "pptSerial": ppt_serial,
                "programId": "",
                "severity": "10"
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        res_data = res.json()["data"]
        return res_data["projectInvalids"]
