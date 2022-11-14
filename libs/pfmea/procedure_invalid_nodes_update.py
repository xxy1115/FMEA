# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_invalid import getInvalid
from common.get_procedure_function import getProcedureFun


class procedureInvalidNodesUpdate(BaseApi):
    def add_procedure_invalid(self, token, product_type, ppp_serial, serial_num, num):
        """
        添加工序功能的失效--从失效库选择多个失效
        :param num: 添加失效的个数
        """
        self.token = token
        res = getInvalid().get_pfmea_invalid(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enInvalidModeName": res[i]["enInvalidMode"], "invalidmodeName": res[i]["invalidmode"],
                 "invalidmodeSerial": res[i]["serialNum"],
                 "occurrence": res[i]["occurrence"], "pppSerial": ppp_serial, "projectFunctionSerial": serial_num,
                 "severity": res[i]["severity"]})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_procedure_invalid(self, token, product_type, serial_num):
        """编辑工序功能/特性下的失效--从失效列表选择第4个失效"""
        self.token = token
        res = getInvalid().get_pfmea_invalid(token, product_type)
        enInvalidMode = res[3]["enInvalidMode"]
        invalidmode = res[3]["invalidmode"]
        invalidmodeSerial = res[3]["serialNum"]
        severity = res[3]["severity"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/updatePfmeaProjectInvalid",
            "json": {
                "enInvalidModeName": enInvalidMode,
                "invalidmodeName": invalidmode,
                "invalidmodeSerial": invalidmodeSerial,
                "serialNum": serial_num,
                "severity": severity
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_procedure_invalid(self, token, ppp_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/delete",
            "json": {
                "invalidModeSerial": "",
                "isElementInvalidMode": False,
                "isRootInvalid": False,
                "pfaSerial": "",
                "pppSerial": ppp_serial,
                "serialNum": serial_num,
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def add_procedure_feature_invalid(self, token, product_type, ppp_serial, serial_num, num):
        """
        添加工序特性的失效--从失效库选择多个失效
        :param num: 添加失效的个数-3
        """
        self.token = token
        res = getInvalid().get_pfmea_invalid(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectInvalid/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enInvalidModeName": res[i]["enInvalidMode"], "invalidmodeName": res[i]["invalidmode"],
                 "invalidmodeSerial": res[i]["serialNum"],
                 "occurrence": res[i]["occurrence"], "pppSerial": ppp_serial, "projectFeatureSerial": serial_num,
                 "severity": res[i]["severity"]})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

