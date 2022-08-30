# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_invalid import getInvalid
from common.get_measure_d import getMeasureD
from common.get_measure_p import getMeasureP


class measureNodesUpdate(BaseApi):
    def add_measure_nodes(self, data, token, product_type, pid_serial, pif_serial):
        self.token = token
        for item in data["api"]["json"]:
            measures_name = item["measuresName"]
            res = []
            if item["measuresType"] == 0 or item["measuresType"] == 2:
                res = getMeasureP().get_measure_p(token, product_type, measures_name)  # 查询措施名称获取措施信息
                item["occurrence"] = res[0]["occurrence"]
            else:
                res = getMeasureD().get_measure_d(token, product_type, measures_name)
                item["det"] = res[0]["det"]
            item["enMeasuresName"] = res[0]["enMeasure"]
            item["measuresSerial"] = res[0]["serialNum"]  # 获取要添加的措施serialNum
            item["pidSerial"] = pid_serial
            item["pifSerial"] = pif_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        res_data = json.loads(res.json()["data"])
        flag = res_data["flag"]
        change_reason_list = res_data["changeReasonList"]
        project_measures = json.loads(res_data["projectMeasures"])
        return [flag, change_reason_list, project_measures]

    def edit_measure_nodes(self, data, token, product_type, pid_serial, serial_num, project_serial, ppt_serial):
        self.token = token
        measures_name = data["api"]["json"]["measuresName"]
        measures_type = data["api"]["json"]["measuresType"]
        if measures_type == "0" or measures_type == "2":
            res = getMeasureP().get_measure_p(token, product_type, measures_name)  # 查询措施名称获取措施信息
            data["api"]["json"]["occurrence"] = res[0]["occurrence"]
        else:
            res = getMeasureD().get_measure_d(token, product_type, measures_name)
            data["api"]["json"]["det"] = res[0]["det"]
        data["api"]["json"]["enMeasuresName"] = res[0]["enMeasure"]
        data["api"]["json"]["measuresSerial"] = res[0]["serialNum"]
        data["api"]["json"]["serialNum"] = serial_num
        data["api"]["json"]["pidSerial"] = pid_serial
        data["api"]["json"]["projectSerial"] = project_serial
        data["api"]["json"]["pptSerial"] = ppt_serial
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result

    def del_measure_nodes(self, token, measure_name, pid_serial, serial_num, reason_name,
                          ppt_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectMeasure/delete",
            "json": {
                "invalidMode": reason_name,  # 受冲击变形或者断裂(O:3,D:3)未加(O:3,D:3)
                "measure": measure_name,  # 同上
                "measureType": 0,
                "measuresFrom": "0",
                "pidSerial": pid_serial,
                "pifSerial": "",
                "pptSerial": ppt_serial,
                "serialNum": serial_num,
                "sync": True
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
