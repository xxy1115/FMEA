# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_procedure import getProcedure


class elementNodesUpdate(BaseApi):
    def add_element_nodes(self, token, product_type, ppp_serial, num):
        """
        添加要素--从要素库选择多个要素
        :param num: 添加要素的个数-3
        """
        self.token = token
        res = getElement().get_element(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/projectElement/save",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"element": res[i]["element"], "elementType": res[i]["elementType"], "enElement": res[i]["enElement"],
                 "isupdate": True, "modelSpecification": res[i]["modelSpecification"],
                 "procedureElementSerial": res[i]["serialNum"], "projectProcedureSerial": ppp_serial,
                 "remark": res[i]["remark"]
                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_element_nodes(self, token, product_type, serial_num):
        """编辑要素--从要素库列表选择第4个要素"""
        self.token = token
        res = getElement().get_element(token, product_type)
        element = res[3]["element"]
        elementType = res[3]["elementType"]
        enElement = res[3]["enElement"]
        modelSpecification = res[3]["modelSpecification"]
        procedureElementSerial = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/projectElement/updateProjectElement",
            "json": {
                "element": element,
                "elementType": elementType,
                "enElement": enElement,
                "modelSpecification": modelSpecification,
                "procedureElementSerial": procedureElementSerial,
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

    def del_element_nodes(self, token, serial_num,projectProcedureSerial):
        self.token = token
        data = {
            "method": "post",
            "url": f"/gateway/fmea-pfmea/projectElement/delete/{projectProcedureSerial}",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
