# -*- coding: UTF-8 -*-

from common.base import BaseApi
from common.get_max_num import getMaxNum

class addProgram(BaseApi):
    def add_program(self, token, user_id, user_name, product, *dicts):
        """
        新建项目
        :param data: *dict--字典:010车型;001平台
        :return:[项目序列号，项目编号]
        """
        # cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.token = token
        program_num = getMaxNum().get_max_num(token, "program", "program_num", "PN")
        model, platform = dicts
        data = {
            "method": "post",
            "url": "/program_end/program/saveOrUpdate",
            "json": {
                "columns": [],
                "startDate": "2023-07-25",
                "endDate": "2023-08-05",
                "model": model[0]["code"],  # 车型(取第一个选项)
                "productId": product["productId"],
                "productModel": f'产品型号{program_num}',
                "platform": platform[0]["code"],  # 平台(取第一个选项)
                "productName": product["productName"],
                "productNum": product["productNum"],
                "programName": f'项目名称{program_num}',
                "programNum": f'{program_num}',
                "programOwner": user_id,
                "programOwnerName": user_name,
                "programType": f'项目类型{program_num}'
            }
        }
        res = self.send(data)
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

    # def get_max_num(self):
    #     """
    #     获取项目编号
    #     :return: 项目编号
    #     """
    #     data = {
    #         "method": "get",
    #         "url": "/fmea/genNum/getMaxNum",
    #         "params": {
    #             "searchTable": "program",
    #             "searchColumn": "program_num",
    #             "searchInitialLetter": "PN",
    #             "defaultNumTail": 1803090001
    #         }
    #     }
    #     res = self.send(data)
    #     max_num = json.loads(res.json()["data"])["maxNum"]
    #     return max_num
