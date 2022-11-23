# -*- coding: UTF-8 -*-
import json
import os
import time
from common.base import BaseApi


class exportFeature(BaseApi):
    def export_feature(self, token, project_serial):
        """
        导出产品特性
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaProductFeature/exportData",
            "data": {
                "pfmeaProjectSerial": project_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        cur_date = time.strftime("-%Y-%m-%d", time.localtime())
        file_name = f'PFMEA产品特性{cur_date}.xls'
        with open(f'pfmea_feature/{file_name}', "wb") as f:
            f.write(res.content)

    def del_last_file(self):
        """删除上次生成的产品特性"""
        name = os.listdir("pfmea_feature")
        print(name)
        for i in name:
            if 'PFMEA产品特性' in i:
                path = f'pfmea_feature/{i}'
                os.remove(path)
