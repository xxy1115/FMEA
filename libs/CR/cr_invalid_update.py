# -*- coding: UTF-8 -*-
import json
import random

from common.base import BaseApi
from common.get_invalid import getInvalid


class crInvalidUpdate(BaseApi):
    def add_cr_invalid(self, token, product_type, pfe_serial, ppt_serial, num):
        self.token = token
        res = getInvalid().get_dfmea_invalid(token, product_type)
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/projectInvalid/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            # 生成32位随机数
            num = []
            for n in range(32):
                num.append(random.choice("1234567890abcdef"))
            cr_id = "".join(num)
            data["json"].append(
                {"crId": cr_id,"enInvalidModeName": res[i]["enInvalidMode"],
                 "invalidmodeName": res[i]["invalidmode"],
                 "invalidmodeSerial": res[i]["serialNum"],
                 "occurrence": res[i]["occurrence"], "pfeSerial": pfe_serial,
                 "pptSerial": ppt_serial, "severity": res[i]["severity"]
                 })
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_cr_invalid(self, token, invalid_name, pif_serial, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/projectInvalid/delete",
            "json": {
                "pidName": invalid_name,
                "serialNum": serial_num
                # "pifSerial": pif_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        return result
