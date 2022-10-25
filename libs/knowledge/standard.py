# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class Standard(BaseApi):
    def save_standard(self, token, customer, standardType, product_types):
        """
        创建技术标准
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        enStandardName = f'Standard{cur_time}'
        enTestProject = f'TestProject{cur_time}'
        standardName = f'标准名称{cur_time}'
        standardNum = f'标准编号{cur_time}'
        technicalRequirement = f'标准要求{cur_time}'
        testMethod = f'检测方法{cur_time}'
        testNum = f'测试编号{cur_time}'
        testProject = f'试验/检测项目{cur_time}'
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/technicalStandard/saveOrUpdate",
            "json": {
                "chapterNum": "要求对应章节编号",
                "customer": customer,
                "enStandardName": enStandardName,
                "enTestProject": enTestProject,
                "fileList": [],
                "obj": product_types,
                "standardName": standardName,
                "standardNum": standardNum,
                "standardType": standardType,
                "standardVersionNum": "V1.0",
                "technicalRequirement": technicalRequirement,
                "testMethod": testMethod,
                "testNum": testNum,
                "testProject": testProject
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_standard(self, token, standard_serial):
        """
        从技术标准库删除指定serialNum的技术标准
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-knowledge/technicalStandard/delete",
            "data": standard_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result