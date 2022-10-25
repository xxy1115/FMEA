# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class processFeature(BaseApi):
    def save_process_feature(self, token, elementType, product_types):
        """
        创建要素失效
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        featureExplain = f'过程特性{cur_time}'
        enFeature = f'PC{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/processFeatureCategory/saveOrUpdate",
            "json": {
                "elementType": elementType,
                "enFeature": enFeature,
                "featureExplain": featureExplain,
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

    def del_process_feature(self, token, ei_serial):
        """
        从要素失效库删除指定serialNum的要素失效
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/processFeatureCategory/delete",
            "data": ei_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
