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
            "url": "/gateway/fmea-dfmea/dfmeaRecordExport/dfmeaRecordExport",
            "data": {
                "pptSerial": ppt_serial,
                "exportType": exportType,  # 导出类型（pdf/excel）
                "exportLangType": exportLangType,  # 导出的语言（1中文、2英文、3中英文）
                "selectedRange": selectedRange,  # 导出选项
                "dfmeaExportType": dfmeaExportType,  # 格式类型（1、标准、2新版）
                "dfmeaViewType": dfmeaViewType  # 导出视图（1合并、2单行）
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
