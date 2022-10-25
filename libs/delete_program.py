# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class deleteProgram(BaseApi):
    def delete_program(self, token, serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-program/program/delete",
            "data": serial_num
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
