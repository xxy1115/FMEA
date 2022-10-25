# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_procedure_function import getProcedureFun


class procedureFunNodesUpdate(BaseApi):
    def add_procedure_fun(self, token, product_type, pp_serial, num):
        """
        添加工序功能--从工序功能库选择多个工序功能
        :param num: 添加工序功能的个数-3
        """
        self.token = token
        res = getProcedureFun().get_procedure_fun(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectFunction/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enFunction": res[i]["enFunction"], "functionType": res[i]["functionType"], "procedureFunctionName": res[i]["function"],
                 "procedureFunctionSerial": res[i]["serialNum"], "projectProcedureSerial": pp_serial})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_procedure_fun(self, token, product_type, serial_num):
        """编辑工序功能--从工序功能列表选择第4个工序功能"""
        self.token = token
        res = getProcedureFun().get_procedure_fun(token, product_type)
        enFunction = res[3]["enFunction"]
        function = res[3]["function"]
        procedureFunctionSerial = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProjectFunction/updatePfmeaProjectFunction",
            "json": {
                "enFunction": enFunction,
                "procedureFunctionName": function,
                "procedureFunctionSerial": procedureFunctionSerial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_procedure_fun(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/gateway/fmea-pfmea/pfmeaProjectFunction/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
