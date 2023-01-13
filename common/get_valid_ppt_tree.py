# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getValidPptTree(BaseApi):
    def get_valid_ppt_tree(self, token, project_serial,search_key=""):
        """
        选择介质
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/project/getValidPptTreeByProjectSerial",
            "json": {
                "projectSerial": project_serial,
                "searchValue": search_key,
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        tree = res.json()["data"]["tree"]
        return tree
