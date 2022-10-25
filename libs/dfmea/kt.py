# -*- coding: UTF-8 -*-
import json
import random

from common.base import BaseApi
from common.get_interface import getInterface
from common.get_valid_ppt_tree import getValidPptTree


class KT(BaseApi):
    def get_all_Kt_new(self, token, ppt_serials):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/project/getAllKtNodeNew",
            "json": ppt_serials
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result

    def get_kt(self, token, project_serial, ppt_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/ktNew/getKt",
            "json": {
                "currentPptSerial": ppt_serial,
                "projectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result

    def save_kt_data(self, token, ppt_serial, project_serial, kt_serial, ktNodeList, ktNodes):
        self.token = token
        # 获取界面功能信息
        res = getInterface().get_interface(token)
        enInterfaceDescribe = res[0]["enInterfaceDescribe"]
        interfaceDescribe = res[0]["interfaceDescribe"]
        interfaceDescribeSerial = res[0]["serialNum"]
        # 获取介质信息
        res = getValidPptTree().get_valid_ppt_tree(token, project_serial)
        middleNodeName = res[0]["productName"]
        middleNodeSerial = res[0]["serialNum"]
        enMiddleNodeName = res[0]["product"]["enProductName"]
        # 传入连线的两个产品节点信息
        ktNodeName1 = ktNodes[0]["productName"]
        ktNodeName2 = ktNodes[1]["productName"]
        ktNodeSerial1 = ktNodes[0]["serialNum"]
        ktNodeSerial2 = ktNodes[1]["serialNum"]
        # 生成32位随机数
        num = []
        for i in range(32):
            num.append(random.choice("1234567890abcde"))
        new_line_serial = "".join(num)
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/ktNew/saveKtData",
            "json": {
                "affirmLineList": [{"serialNum": new_line_serial}],
                "currentPptSerial": ppt_serial,
                "deleteLineList": [],
                "deleteNodeList": [],
                "kt": {
                    "pptSerial": ppt_serial,
                    "projectSerial": project_serial,
                    "serialNum": kt_serial
                },
                "locList": [],
                "modifyLineList": [],
                "newLineList": [{
                    "currentPptSerial": ppt_serial,
                    "enInterfaceDescribe": enInterfaceDescribe,
                    "enMiddleNodeName": enMiddleNodeName,
                    "field2": 1,
                    "interfaceDescribe": interfaceDescribe,
                    "interfaceDescribeSerial": interfaceDescribeSerial,
                    "ktNodeName1": ktNodeName1,
                    "ktNodeName2": ktNodeName2,
                    "ktNodeSerial1": ktNodeSerial1,
                    "ktNodeSerial2": ktNodeSerial2,
                    "ktSerial": kt_serial,
                    "lineType": 1,  # 界面类型(1-7)
                    "linkCategory": "b",
                    "middleNodeName": middleNodeName,
                    "middleNodeSerial": middleNodeSerial,
                    "projectSerial": project_serial,
                    "serialNum": new_line_serial,
                    "surfaceType": "II"  # 内部界面，没用到
                }],
                "newNodeList": [],
                "newProductList": [],
                "replaceNodeList": []
            }
        }
        for i, item in enumerate(ktNodeList):
            data["json"]["locList"].append(
                {"height": item["height"], "id": item["id"], "left": item["left"], "pptSerial": item["pptSerial"],
                 "serialNum": item["serialNum"], "top": item["top"],
                 "width": item["width"]})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return result

    # def save_line_type(self, token, project_node_serial, project_serial):
    #     self.token = token
    #     data = {
    #         "method": "post",
    #         "url": "/fmea/dfmeaBlockDiagramLineType/saveOrUpdateLineType",
    #         "json": {
    #             "lineType": "orthogonalLink",  # default-弧线;orthogonalLink-折线
    #             "projectNodeSerial": project_node_serial,
    #             "projectSerial": project_serial
    #         }
    #     }
    #     res = self.send(data)
    #     if res.status_code != 200:
    #         return False
    #     else:
    #         return True
