# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class Interface(BaseApi):
    def save_interface(self, token, type):
        """
        创建界面功能
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        enInterfaceDescribe = f'IF{cur_time}'
        interfaceDescribe = f'界面描述{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/interfaceDescribe/saveOrUpdate",
            "json": {
                "enInterfaceDescribe": enInterfaceDescribe,
                "interfaceDescribe": interfaceDescribe,
                "interfaceDescribeType": type
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_interface(self, token, IF_serial):
        """
        从界面功能库删除指定serialNum的界面功能
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/interfaceDescribe/delete",
            "data": IF_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result