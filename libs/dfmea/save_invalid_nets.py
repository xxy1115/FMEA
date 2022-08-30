# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class saveInvalidNets(BaseApi):
    # 添加下级零件失效作为失效原因/添加上级零件失效作为失效后果
    def save_invalid_nets(self, token, first, second, flag=0, consequence_type=""):
        self.token = token
        data = {
            "method": "post",
            "url": "/fmea/invalidNet/saveProjectInvalidNets",
            "json": []
        }
        if flag == 0:
            data["json"].append({
                "det": "10",
                "edituser": 1,
                "firstPfSerial": first["pfSerial"],
                "firstPidSerial": first["serialNum"],
                "firstPifSerial": first["pifSerial"],
                "firstPptSerial": first["pptSerial"],
                "occurrence": second["occurrence"],
                "pifSerial": "",
                "projectMeasuresList": [],
                "reasonName": second["invalidmodeName"],
                "secondPfSerial": second["pfSerial"],
                "secondPfeSerial": second["pfeSerial"],
                "secondPidSerial": second["serialNum"],
                "secondPifSerial": second["pifSerial"],
                "secondPptSerial": second["pptSerial"],
                "severity": first["severity"],
                "type": "1"
            })
        else:
            data["json"].append({
                "consequenceType": consequence_type,
                "det": "10",
                "edituser": 2,
                "firstPfSerial": first["pfSerial"],
                "firstPfeSerial": first["pfeSerial"],
                "firstPidSerial": first["serialNum"],
                "firstPifSerial": first["pifSerial"],
                "firstPptSerial": first["pptSerial"],
                "occurrence": 10,
                "pifSerial": "",
                "secondPfSerial": second["pfSerial"],
                "secondPidSerial": second["serialNum"],
                "secondPptSerial": second["pptSerial"],
                "severity": first["severity"],
                "type": "2"
            })
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = json.loads(res.json()["data"])
        if result["flag"] and result["flag"] != True:
            return False
        return result["projectInvalidNets"]
