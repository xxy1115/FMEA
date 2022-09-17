# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class procedureElement(BaseApi):
    def save_procedure_element(self, token, elementType, product_types):
        """
        创建工序要素
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        element = f'工序要素{cur_time}'
        enElement = f'PE{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/procedureElement/saveOrUpdate",
            "json": {
                "element": element,
                "elementType": elementType,
                "enElement": enElement,
                "modelSpecification": "工序要素规格/型号",
                "productTypes": product_types
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_procedure_element(self, token, pe_serial):
        """
        从工序要素库删除指定serialNum的工序要素
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/procedureElement/delete",
            "data": pe_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
