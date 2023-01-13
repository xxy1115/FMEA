# -*- coding: UTF-8 -*-
import json
import random

from common.base import BaseApi
from common.get_feature import getFeature


class crFeatureUpdate(BaseApi):
    def add_cr_feature(self, token, product_type, pf_serial, num):
        self.token = token
        res = getFeature().get_feature(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/projectFeature/saveFeatures",
            "json": []
        }
        for i in range(num):
            # 生成32位随机数
            num = []
            for n in range(32):
                num.append(random.choice("1234567890abcdef"))
            cr_id = "".join(num)
            data["json"].append(
                {"controlFeature": 1, "crId": cr_id, "enFeature": res[i]["enFeature"],
                 "feature": res[i]["featureExplain"],
                 "featureSymbolSerial": "", "pfSerial": pf_serial, "productFeatureSerial": res[i]["serialNum"],
                 "technicalRequirements": f"技术要求{i + 1}"
                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result["projectFeatureList"]

    def del_cr_feature(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectFeature/deleteFeature",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result["flag"]
