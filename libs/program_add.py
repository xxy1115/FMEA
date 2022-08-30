# -*- coding: UTF-8 -*-
import json
import time

from common.base import BaseApi


class addProgram(BaseApi):
    def add_program(self, data, product, token, user_id, *dicts):
        """
        新建项目
        :param data: *dict--字典:010车型;001平台
        :return:[项目序列号，项目编号]
        """
        # cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.token = token
        program_num = self.get_max_num()
        model, platform = dicts
        data["api"]["json"]["programNum"] = program_num
        data["api"]["json"]["programOwner"] = user_id
        data["api"]["json"]["model"] = model[0]["code"]  # 车型(取第一个选项)
        data["api"]["json"]["platform"] = platform[0]["code"]  # 平台(取第一个选项)
        data["api"]["json"]["productModel"] = f'产品型号{program_num}'  # 产品型号
        data["api"]["json"]["programName"] = f'项目名称{program_num}'  # 项目名称
        data["api"]["json"]["programType"] = f'项目类型{program_num}'  # 项目类型
        data["api"]["json"]["productId"] = product["productId"]  # 产品ID
        data["api"]["json"]["productNum"] = product["productNum"]  # 产品编号
        data["api"]["json"]["productName"] = product["productName"]  # 产品名称
        res = self.send(data["api"])
        if res.status_code != 200:
            return False
        serial_num = res.json()["data"]["serialNum"]
        # self.select_program_by_id(serial_num)
        return [serial_num, program_num]

    # def select_program_by_id(self, serial_num):
    #     data = {
    #         "method": "get",
    #         "url": "/program_end/program/selectProgramById",
    #         "params": {"serialNum": "serial_num"}
    #     }
    #     res = self.send(data)
    #     program_data = json.loads(res.json()["data"])["program"]
    #     return program_data

    def get_max_num(self):
        """
        获取项目编号
        :return: 项目编号
        """
        data = {
            "method": "get",
            "url": "/fmea/genNum/getMaxNum",
            "params": {
                "searchTable": "program",
                "searchColumn": "program_num",
                "searchInitialLetter": "PN",
                "defaultNumTail": 1803090001
            }
        }
        res = self.send(data)
        max_num = json.loads(res.json()["data"])["maxNum"]
        return max_num
