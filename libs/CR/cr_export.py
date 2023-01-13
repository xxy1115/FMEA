# -*- coding: UTF-8 -*-
import os

from common.base import BaseApi


class crExport(BaseApi):
    def cr_export(self, token, project_serial, file_name):
        """
        导出客户要求
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/exportCR",
            "data": {
                "serialNum": "-1",
                "projectSerial": project_serial,
                "SelfExport": "true"
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        with open(f'customer_request/{file_name}', "wb") as f:
            f.write(res.content)

    def del_last_export(self):
        """删除上次导出的客户要求"""
        name = os.listdir("customer_request")
        print(name)
        for i in name:
            if '客户要求-' in i:
                path = f'customer_request/{i}'
                os.remove(path)
