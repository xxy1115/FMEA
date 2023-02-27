# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class BOM(BaseApi):
    def is_has_children(self, token, project_serial):
        """
        判断DFMEA项目是否包含子零件
        :param token:
        :return:1-不包含子零件；2-包含子零件
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/isProjectHasNodeChildren",
            "data": project_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result["flag"]

    def bom_list(self, token, product_Id, search_key=""):
        """
        加载BOM导入列表
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/list",
            "json": {
                "from": -1,
                "pageSize": -1,
                "productCategorys": [],
                "productId": product_Id,
                "productTypes": [],
                "searchKey": search_key,
                "sort": "",
                "sortColumn": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        items = res.json()["data"]["items"]
        return items

    def import_bom(self, token, project_serial, bom_serial, ppt_serial):
        """
        导入BOM
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-dfmea/projectBom/importBomToProject",
            "params": {
                "projectSerial": project_serial,
                "bomSerial": bom_serial,
                "pptSerial": ppt_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def get_bom_list_by_serialNum(self, token, project_serial):
        """获取bom列表"""
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-dfmea/bomList/getBomListBySerialNum",
            "params": {
                "serialNum": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result["bomList"]["children"]

    def import_excel(self, token, project_serial):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/bomList/bomImport",
            "files": {"excelFile": ("bom_v7.xls", open("bom_v7.xls", "rb"), "application/vnd.ms-excel")},
            "data": {
                "projectSerial": project_serial,
                "pptSerial": "",
                "programId": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result["data"]
