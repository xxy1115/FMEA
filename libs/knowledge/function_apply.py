# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi
from common.get_function import getFunction


class functionApply(BaseApi):
    def function_apply(self, token, username, function_serial, function_name, product_type):
        """
        功能提交审核
        :param token:
        :return:
        """
        self.token = token
        res = getFunction().get_function(token, product_type, function_name)
        functionId = res[0]["functionId"]
        data = {
            "method": "post",
            "url": "/knowledge_end/function/apply",
            "json": {
                "applyRemark": "备注",
                "functionIds": functionId,
                "ids": function_serial,
                "lanTuMessageType": "0",
                "receiver": username
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def function_approve(self, token, username, function_serial, function_name, product_type):
        """
        功能审核通过
        :return:
        """
        self.token = token
        res = getFunction().get_function(token, product_type, function_name)
        functionId = res[0]["functionId"]
        data = {
            "method": "post",
            "url": "/knowledge_end/function/approve",
            "json": {
                "approveRemark": "同意",
                "approveState": "0",
                "functionIds": functionId,
                "ids": function_serial,
                "receiver": username
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
