# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class frequencyRating(BaseApi):
    def save_frequency_rating(self, token, product_types):
        """
        创建频率评级措施
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        measure = f'频率评级措施{cur_time}'
        enMeasure = f'frequency{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/knowledgeFrequencyRatingMeasure/saveOrUpdate",
            "json": {
                "enMeasure": enMeasure,
                "frequency":"5",
                "measure": measure,
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

    def del_frequency_rating(self, token, frequency_measure_serial):
        """
        从删除指定serialNum的频率评级措施
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/knowledgeFrequencyRatingMeasure/delete",
            "data": frequency_measure_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
