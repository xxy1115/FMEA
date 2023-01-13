# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_max_num import getMaxNum


class addDFMEATemplate(BaseApi):
    def add_dfmea_template(self, data, product, program, token, user_id, user_name, *dicts):
        """
        新建DFMEA
        :param data:
        :return:
        """
        self.token = token
        platform, customer, secrecyGrade, module = dicts
        project_num = getMaxNum().get_max_num(token, "project", "project_num", "TD")
        data["api"]["json"]["owner"] = user_id  # 当前用户ID
        data["api"]["json"]["ownerName"] = user_name  # 当前用户名
        data["api"]["json"]["platform"] = platform[0]["code"]  # 平台
        data["api"]["json"]["customer"] = customer[0]["code"]  # 客户
        data["api"]["json"]["secrecyGrade"] = secrecyGrade[0]["code"]  # 保密等级
        data["api"]["json"]["productId"] = product["productId"]  # 产品ID
        data["api"]["json"]["productNum"] = product["productNum"]  # 产品编号
        data["api"]["json"]["productName"] = product["productName"]  # 产品名称
        all_column = self.get_column_list()
        column = []
        for item in all_column:
            if item["columnName"] == "产品型号":
                item["value"] = "产品型号" + project_num
                column.append(item)
            if item["columnName"] == "整车源码":
                item["value"] = "整机源码" + project_num
                column.append(item)
            if item["columnName"] == "公司名称":
                item["value"] = "公司名称" + project_num
                column.append(item)
            if item["columnName"] == "项目地点":
                item["value"] = "项目地点" + project_num
                column.append(item)
            if item["columnName"] == "模块":
                item["value"] = module[0]["code"]  # 模块
                column.append(item)
            if item["columnName"] == "流程启动人":
                item["value"] = ""
                column.append(item)
        data["api"]["json"]["columns"] = column
        data["api"]["json"]["projectNum"] = project_num  # FMEA编号
        data["api"]["json"]["projectName"] = f'AT_{project_num}'  # FMEA名称
        data["api"]["json"]["enProgramName"] = program["programName"]  # 项目名称
        data["api"]["json"]["programName"] = program["programName"]  # 项目名称
        data["api"]["json"]["programNum"] = program["programNum"]  # 项目编号
        data["api"]["json"]["programOwner"] = program["creator"]  # 项目负责人编号
        data["api"]["json"]["programOwnerName"] = program["creatorName"]  # 项目负责人
        data["api"]["json"]["programSerial"] = program["serialNum"]  # 项目序列号
        data["api"]["json"]["remark"] = f'备注_{project_num}'  # 备注
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data

    def get_column_list(self):
        data = {
            "method": "get",
            "url": "/gateway/fmea-system/tableColumn/getColumnList",
            "params": {"category": "addDfmea"}
        }
        res = self.send(data)
        column_list = json.loads(res.json()["data"])["items"]
        return column_list

    def save_template(self, token, ppt_serial, product_id, product_name, project_name, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/productTemplate/saveOrUpdateTemplate",
            "json": {
                "pptSerialNum": ppt_serial,
                "productId": product_id,
                "projectType": "dfmea",
                "remark": "备注",
                "sourceNodeName": product_name,
                "sourceProjectName": project_name,
                "templateName": project_name,
                "templateProjectName": project_name,
                "templateProjectSerialNum": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        res_data = res.json()["data"]
        return res_data
