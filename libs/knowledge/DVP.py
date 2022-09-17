# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class DVP(BaseApi):
    def save_DVP(self, token, dvpLayer, product_types):
        """
        创建DVP
        :param token:
        :return:
        """
        self.token = token
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        enStandardName = f'StandardName{cur_time}'
        standardName = f'标准名称{cur_time}'
        dvpName = f'试验/检验项目{cur_time}'
        enDvpName = f'DVPName{cur_time}'
        dvpGoal = f'实验目的{cur_time}'
        dvpEquipment = f'实验设备{cur_time}'
        dvpPeriod = f'实验周期{cur_time}'
        validateParameter = f'验证参数{cur_time}'
        dvpScheme = f'试验/检验方法{cur_time}'
        data = {
            "method": "post",
            "url": "/knowledge_end/dvpStandard/saveOrUpdate",
            "json": {
                "standardName": standardName,
                "enStandardName": enStandardName,
                "dvpName": dvpName,
                "dvpLayer": dvpLayer,
                "dvpGoal": dvpGoal,
                "enDvpName": enDvpName,
                "dvpObjs": product_types,
                "dvpEquipment": dvpEquipment,
                "dvpPeriod": dvpPeriod,
                "validateParameter": validateParameter,
                "dvpScheme": dvpScheme,
                "dvpCriteria": "判断标准",
                "sampleName": "样件名称",
                "sampleCount": "1000"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        flag = res.json()["data"]["flag"]
        return [flag, dvpName]

    def search_DVP(self, token, product_type, search_key=""):
        """
        DVP列表查询
        :param token:
        :return:DVP列表数组
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/dvpStandard/list",
            "json": {
                "endTime": "",
                "experienceType": "",
                "fieldKey": "",
                "fieldValue": "",
                "from": 0,
                "functionTypes": [],
                "isUpProduct": "",
                "measureClassifyList": [],
                "pageSize": 10,
                "pfSerial": "",
                "pifSerial": "",
                "pptSerial": "",
                "problemStatus": "",
                "productCategorys": [],
                "productId": "",
                "productIds": [],
                "productTypeList": product_type,
                "productTypes": [],
                "projectSerial": "",
                "searchId": "",
                "searchKey": search_key,
                "serialNums": "",
                "sort": "",
                "sortColumn": "",
                "sortValue": "",
                "status": "",
                "statusTime": "",
                "type": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        lists = res.json()["data"]["items"]
        return lists


    def del_DVP(self, token, DVP_serial):
        """
        从DVP库删除指定serialNum的DVP
        :param token:
        :param function_serial:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/knowledge_end/dvpStandard/delete",
            "data": DVP_serial
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
