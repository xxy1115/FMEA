# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class savePfRelation(BaseApi):
    # 保存功能关联
    def save_pf_relation(self, token, first_pf_serial, second_pf_serial, second_pfe_serial):
        """
        添加下级零件失效作为失效原因时保存功能关联
        :param first_pf_serial:
        :param second_pf_serial:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/ktNew/forEachSaveGnjmjzPfRelation",
            "json": {
                "parentPfSerial": first_pf_serial,
                "pfSerials": [second_pf_serial],
                "pfeSerials": [second_pfe_serial]
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result

    def save_consequence_pf_relation(self, token, first_pf_serial, first_pfe_serial, second_pf_serial):
        """
        添加上级零件失效作为失效后果时保存功能关联
        :param first_pf_serial:
        :param second_pf_serial:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/ktNew/saveConsequenceGnjmjzPfRelation",
            "json": {
                "parentPfSerials": [first_pf_serial],
                "parentPfeSerials": [first_pfe_serial],
                "pfSerial": second_pf_serial
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
