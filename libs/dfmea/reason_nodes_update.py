# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_invalid import getInvalid


class reasonNodesUpdate(BaseApi):
    def add_reason_nodes(self, data, token, product_type, node_data):
        self.token = token
        for item in data["api"]["json"]:
            invalid_name = item["invalidmodeName"]
            res = getInvalid().get_invalid(token, product_type, invalid_name)  # 查询失效名称获取失效信息
            item["enInvalidModeName"] = res[0]["enInvalidMode"]
            item["invalidmodeSerial"] = res[0]["serialNum"]  # 获取要添加的失效serialNum
            item["occurrence"] = res[0]["occurrence"]
            item["severity"] = node_data["severity"]  # 严重度作为后果，取上级失效的严重度
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        project_invalids = result["projectInvalids"]
        # 获取失效网
        project_invalid_nets = self.save_invalid_nets(project_invalids, node_data, token)
        # 获取功能网
        save_pf_relation = self.save_pf_relation(token, node_data["pfSerial"])
        return [project_invalids, project_invalid_nets, save_pf_relation]

    def save_pf_relation(self, token, pf_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/ktNew/forEachSaveGnjmjzPfRelation",
            "json": {
                "parentPfSerial": pf_serial,
                "pfSerials": [],
                "pfeSerials": []
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result

    def save_invalid_nets(self, project_invalids, node_data, token):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/saveProjectInvalidNets",
            "json": []
        }
        for i, item in enumerate(project_invalids):
            data["json"].append({"det": "10", "edituser": str(i + 1), "firstPfSerial": node_data["pfSerial"],
                                 "firstPidSerial": node_data["serialNum"], "firstPptSerial": node_data["pptSerial"],
                                 "occurrence": item["occurrence"], "reasonName": item["invalidmodeName"],
                                 "secondPidSerial": item["serialNum"], "severity": node_data["severity"], "type": "1"})
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["projectInvalidNets"]

    def edit_reason_nodes(self, data, token, product_type, serial_num):
        self.token = token
        invalid_name = data["api"]["json"]["invalidmodeName"]
        res = getInvalid().get_invalid(token, product_type, invalid_name)  # 查询失效名称获取功能信息
        data["api"]["json"]["enInvalidModeName"] = res[0]["enInvalidMode"]
        data["api"]["json"]["invalidmodeSerial"] = res[0]["serialNum"]
        data["api"]["json"]["occurrence"] = res[0]["occurrence"]
        data["api"]["json"]["severity"] = res[0]["severity"]
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        edit_res = json.loads(res.json()["data"])
        second_pid_serial = edit_res["projectInvalid"]["serialNum"]
        update_invalid_nets = self.update_invalid_nets(token, second_pid_serial, serial_num)
        return update_invalid_nets

    def update_invalid_nets(self, token, second_pid_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/updateDfmeaProjectInvalidNet",
            "json": {
                "secondPfSerial": "",
                "secondPidSerial": second_pid_serial,
                "secondPifSerial": "",
                "secondPptSerial": "",
                "serialNum": serial_num,
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["projectInvalidNet"]

    def del_reason_nodes(self, token, name, pif_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/delete",
            "json": {
                "name": name,
                "pifSerial": pif_serial,
                "serialNum": serial_num,
                "type": "1"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
