# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_procedure import getProcedure
from common.get_product import getProduct


class procedureNodesUpdate(BaseApi):
    def add_procedure_nodes(self, token, product_type, project_serial, ppp_serial, num):
        self.token = token
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProcessProcedure/save",
            "json": []
        }
        res = getProcedure().get_procedure(token, product_type)
        for i in range(num):
            data["json"].append({"level": 1, "parentProjectProcedureSerial": ppp_serial, "ppSerial": "-1", "processNo": f"OP{i*10}",
                                 "processProcedureId": res[i]["serialNum"], "projectSerial": project_serial, "sort": f"{i*10}"
                                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_procedure_nodes(self, data, token, product_type, serial_num):
        self.token = token
        parts_name = data["api"]["json"]["partsName"]
        res = getProduct().get_product(token, product_type, parts_name)  # 获取指定产品名称的产品信息
        data["api"]["json"]["productId"] = res[0]["productId"]  # 取产品名称匹配的第一个产品ID
        data["api"]["json"]["serialNum"] = serial_num
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]

    def del_procedure_nodes(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/project/delProductNodes",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
