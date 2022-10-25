# -*- coding: UTF-8 -*-
import json
import os
import time

from common.base import BaseApi


class exportReport(BaseApi):
    def export_report(self, token, ppt_serial, exportType, exportLangType, selectedRange, dfmeaExportType,
                      dfmeaViewType, file_name):
        """
        导出DFMEA报告
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/dfmeaRecordExport/dfmeaRecordExport",
            "data": {
                "pptSerial": ppt_serial,
                "exportType": exportType,
                "exportLangType": exportLangType,
                "selectedRange": selectedRange,
                "dfmeaExportType": dfmeaExportType,
                "dfmeaViewType": dfmeaViewType
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        with open(f'dfmea_report/{file_name}', "wb") as f:
            f.write(res.content)

    def del_last_report(self):
        """删除上次生成的DFMEA报告"""
        name = os.listdir("dfmea_report")
        print(name)
        for i in name:
            if 'dfmea_report' in i:
                path = f'dfmea_report/{i}'
                os.remove(path)
