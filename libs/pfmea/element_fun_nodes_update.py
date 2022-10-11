# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun


class elementFunNodesUpdate(BaseApi):
    def add_element_fun_nodes(self, token, product_type, pe_serial, num):
        """
        添加要素功能--从要素功能库选择多个要素功能
        :param num: 添加要素功能的个数-3
        """
        self.token = token
        res = getElementFun().get_element_fun(token, product_type)
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectElementFunction/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"elementFunction": res[i]["function"], "elementFunctionSerial": res[i]["serialNum"],
                 "enFunction": res[i]["enFunction"],
                 "functionType": res[i]["functionType"], "projectElementSerial": pe_serial})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_element_fun_nodes(self, token, product_type, serial_num):
        """编辑要素功能--从要素库功能列表选择第4个要素功能"""
        self.token = token
        res = getElementFun().get_element_fun(token, product_type)
        function = res[3]["function"]
        elementFunctionSerial = res[3]["serialNum"]
        enFunction = res[3]["enFunction"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectElementFunction/updateProjectElementFunction",
            "json": {
                "elementFunction": function,
                "elementFunctionSerial": elementFunctionSerial,
                "enFunction": enFunction,
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

    def del_element_fun_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/pfmea_end/pfmeaProjectElementFunction/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
