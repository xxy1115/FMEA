# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_invalid import getInvalid
from common.get_measure_occ import getMeasureP


class Invalid(BaseApi):
    def get_fault_mode(self, token):
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/failureBasicTerminology/getFaultModeNameList",
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]["faultModeNameList"]
        return result

    def get_function_group(self, token):
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/invalidMode/getFunctionGroupList",
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]["functionGroupList"]
        return result

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
            "url": "/knowledge_end/invalidMode/saveOrUpdate",
            "json": {
                "applicableObject": applicableObject,
                "category": category,
                "enInvalidMode": enInvalidMode,
                "failureClass": failureClass,
                "faultModeName": faultModeName,
                "functionGroupId": functionGroupId,
                "invalidUseType": invalidUseType,
                "invalidmode": invalidmode,
                "occurrence": "10",
                "processCode": "工序代码",
                "productTypes": product_types,
                "rejectRatio": "50%",
                "severity": "10",
                "standardCode": "A101A00001037",
                "uploadAttachmentList": []
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        serial_num = res.json()["data"]["serialNum"]
        return [serial_num, invalidmode]

    def del_invalid(self, token, invalid_serial):
        """
        从失效库删除指定serialNum的失效
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/invalidMode/delete",
            "data": invalid_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def add_invalid_measure(self, token, invalid_serial, product_type):
        """
        在产品失效库中添加措施
        :return:
        """
        self.token = token
        list = getMeasureP().get_measure_p(token, product_type)
        occMeasure_serial = list[0]["serialNum"]  # 获取要添加的预防措施serialNum
        data = {
            "method": "post",
            "url": "/knowledge_end/invalidMode/addInvalidMeasure",
            "json": [{
                "invalidmodeId": invalid_serial,
                "measureId": occMeasure_serial,
                "type": 0
            }]
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def delete_invalid_measure(self, token, product_type, invalidmode):
        """
        删除产品失效库的措施
        :param token:
        :param product_type:
        :param invalidmode:
        :return:
        """
        self.token = token
        list = getInvalid().get_invalid(token, product_type, invalidmode)
        invalid_measure_serial = list[0]["invalidMeasureList"][0]["serialNum"]
        data = {
            "method": "post",
            "url": "/knowledge_end/invalidMode/deleteInvalidMeasure",
            "data": invalid_measure_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
