# -*- coding: UTF-8 -*-
import json
import os
import time

from common.base import BaseApi


class exportPFMEAReport(BaseApi):
    def export_pfmea_report(self, token, ppp_serial, exportType, exportLangType, selectedRange, pfmeaExportType,
                            pfmeaViewType, file_name):
        """
        导出PFMEA报告
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-pfmea/pfmeaRecordExport/pfmeaExport",
            "data": {
                "pppSerial": ppp_serial,
                "exportType": exportType,  # 导出类型（pdf/excel）
                "exportLangType": exportLangType,  # 导出的语言（1中文、2英文、3中英文）
                "selectedRange": selectedRange,  # 导出选项
                "pfmeaExportType": pfmeaExportType,  # 格式类型（1、标准、2新版）
                "pfmeaViewType": pfmeaViewType,  # 导出视图（2单行、1合并）
                "fmeaVersion": "当前版本7.0.1.6（正式版）",
                "isOnlyReport": ""
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        with open(f'pfmea_report/{file_name}', "wb") as f:
            f.write(res.content)

    def del_last_report(self):
        """删除上次生成的PFMEA报告"""
        name = os.listdir("pfmea_report")
        print(name)
        for i in name:
            if 'pfmea_report' in i:
                path = f'pfmea_report/{i}'
                os.remove(path)
