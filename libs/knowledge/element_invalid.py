# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class elementInvalid(BaseApi):
    def save_element_invalid(self, token, elementType, product_types):
        """
        创建要素失效
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        invalidmode = f'要素失效{cur_time}'
        enInvalidMode = f'EI{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/elementInvalid/saveOrUpdate",
            "json": {
                "elementType": elementType,
                "enInvalidMode": enInvalidMode,
                "invalidmode": invalidmode,
                "occurrence": "10",
                "productTypes": product_types,
                "rejectRatio": "50%"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_element_invalid(self, token, ei_serial):
        """
        从要素失效库删除指定serialNum的要素失效
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/elementInvalid/delete",
            "data": ei_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
