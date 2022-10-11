# -*- coding: UTF-8 -*-
import json
from common.base import BaseApi
from common.get_element import getElement
from common.get_element_function import getElementFun
from common.get_element_invalid import getElementInvalid


class elementInvalidNodesUpdate(BaseApi):
    def add_element_invalid_nodes(self, token, product_type, ppp_serial, ef_serial, num):
        """
        添加要素失效--从要素失效库选择多个要素失效
        :param num: 添加要素失效的个数-3
        """
        self.token = token
        res = getElementInvalid().get_element_invalid(token, product_type)
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectInvalid/saveOrUpdate",
            "json": []
        }
        for i in range(num):
            data["json"].append(
                {"enInvalidModeName": res[i]["enInvalidMode"], "invalidmodeName": res[i]["invalidmode"],
                 "invalidmodeSerial": res[i]["serialNum"],
                 "occurrence": res[i]["occurrence"], "pppSerial": ppp_serial, "projectFunctionSerial": ef_serial})
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def edit_element_invalid_nodes(self, token, product_type, serial_num):
        """编辑要素失效--从要素失效列表选择第4个要素失效"""
        self.token = token
        res = getElementInvalid().get_element_invalid(token, product_type)
        enInvalidMode = res[3]["enInvalidMode"]
        invalidmode = res[3]["invalidmode"]
        invalidmodeSerial = res[3]["serialNum"]
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectInvalid/updatePfmeaProjectInvalid",
            "json": {
                "enInvalidModeName": enInvalidMode,
                "invalidmodeName": invalidmode,
                "invalidmodeSerial": invalidmodeSerial,
                "isElementInvalid": True,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result

    def del_element_invalid_nodes(self, token, ppp_serial,serial_num):
        self.token = token
        data = {
            "method": "post",
            "url": f"/pfmea_end/pfmeaProjectInvalid/delete",
            "json": {
                "invalidModeSerial": "",
                "isElementInvalidMode": True,
                "isRootInvalid": False,
                "pfaSerial": "",
                "pppSerial": ppp_serial,
                "serialNum": serial_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
