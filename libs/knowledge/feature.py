# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class Feature(BaseApi):
    def save_feature(self, token, product_types):
        """
        创建特性
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        en_feature = f'Feature{cur_time}'
        feature_explain = f'特性{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/productFeatureCategory/saveOrUpdate",
            "json": {
                "enFeature": en_feature,
                "featureExplain": feature_explain,
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

    def del_feature(self, token, feature_serial):
        """
        从产品特性库删除指定serialNum的产品特性
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/productFeatureCategory/delete",
            "data": feature_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result