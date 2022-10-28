# -*- coding: UTF-8 -*-
from common.base import BaseApi


class bomDetails(BaseApi):
    def get_bom(self, token, serial_num):
        """
        获取基本信息页面数据
        :param token:
        :param serial_num:
        :return:
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-maindata/bom/getBom",
            "params": {
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

    def get_bom_list_by_serialNum(self, token, serial_num):
        """
        获取BOM清单
        :param token:
        :param serial_num:
        :return:
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-maindata/bom/getBomListBySerialNum",
            "params": {
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

    def get_bom_product_by_serialNum(self, token, serial_num):
        """
        获取产品树
        :param token:
        :param serial_num:
        :return:
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/gateway/fmea-maindata/bom/getBomProductByBomSerialNum",
            "params": {
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
