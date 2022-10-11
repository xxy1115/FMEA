# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_procedure import getProcedure
from common.get_product import getProduct


class procedureNodesUpdate(BaseApi):
    def add_procedure_nodes(self, token, product_type, project_serial, ppp_serial, num):
        """
        添加工序--从工序库选择多个工序
        :param num: 添加工序的个数-3
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProcessProcedure/save",
            "json": []
        }
        res = getProcedure().get_procedure(token, product_type)
        for i in range(num):
            data["json"].append({"level": 1, "parentProjectProcedureSerial": ppp_serial, "ppSerial": "-1",
                                 "processNo": f"OP{(i + 1) * 10}",
                                 "processProcedureId": res[i]["serialNum"], "projectSerial": project_serial,
                                 "sort": f"{(i + 1) * 10}"
                                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_procedure_nodes(self, token, product_type, serial_num):
        """编辑工序--从工序库列表选择第4个工序"""
        self.token = token
        res = getProcedure().get_procedure(token, product_type)
        processProcedureId = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectProcedure/update",
            "json": {
                "processProcedureId": processProcedureId,
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

    def del_procedure_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/pfmea_end/pfmeaProcessProcedure/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
