# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_max import getMax
from common.get_max_num import getMaxNum


class addPFMEA(BaseApi):
    def add_pfmea(self, data, token, user_id, user_name, product, related_product, program, procedureName,
                  enProcedureName, customer, secrecyGrade):
        """
        新建PFMEA
        :param data:
        :return:
        """
        self.token = token
        project_num = getMaxNum().get_max_num(token, "pfmea_project", "project_num", "PF")
        pfd_num = getMax().get_max(token, "sys_table_value", "value", "PFD")
        related_products = [{"productId": related_product["productId"]}]
        data["api"]["json"]["customer"] = customer  # 客户
        data["api"]["json"]["enProcedureName"] = enProcedureName  # 工艺英文名称
        data["api"]["json"]["enProgramName"] = program["enProgramName"]  # 项目英文名称
        data["api"]["json"]["owner"] = user_id  # 当前用户ID
        data["api"]["json"]["ownerName"] = user_name  # 当前用户名
        data["api"]["json"]["pfmeaRelatedProducts"] = related_products  # 关联产品
        data["api"]["json"]["procedureName"] = procedureName  # 工艺名称
        data["api"]["json"]["productId"] = product["productId"]
        data["api"]["json"]["productName"] = product["productName"]
        data["api"]["json"]["productNum"] = product["productNum"]
        data["api"]["json"]["productNums"] = related_product["productNum"]
        data["api"]["json"]["programName"] = program["programName"]  # 项目名称
        data["api"]["json"]["programNum"] = program["programNum"]  # 项目编号
        data["api"]["json"]["programOwner"] = program["programOwner"]  # 项目创建人id
        data["api"]["json"]["programOwnerName"] = program["programOwnerName"]  # 项目创建人姓名
        data["api"]["json"]["programSerial"] = program["serialNum"]  # 项目serialNum
        data["api"]["json"]["projectDescription"] = f'备注{project_num}'
        data["api"]["json"]["projectName"] = f'AT_{project_num}'
        data["api"]["json"]["projectNum"] = project_num
        data["api"]["json"]["secrecyGrade"] = secrecyGrade
        all_column = self.get_column_list()
        column = []
        for item in all_column:
            if item["columnName"] == "过程流程图编号":
                item["value"] = pfd_num
                column.append(item)
            if item["columnName"] == "年型/项目":
                item["value"] = "年型/项目" + project_num
                column.append(item)
            if item["columnName"] == "关联产品":
                item["value"] = ""
                column.append(item)
            if item["columnName"] == "产品型号":
                item["value"] = "产品型号" + project_num
                column.append(item)
        data["api"]["json"]["columns"] = column
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def get_column_list(self):
        data = {
            "method": "get",
            "url": "/fmea/tableColumn/getColumnList",
            "params": {"category": "addPfmea"}
        }
        res = self.send(data)
        column_list = json.loads(res.json()["data"])["items"]
        return column_list
