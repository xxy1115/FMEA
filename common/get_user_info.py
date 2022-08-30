# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class getUserInfo(BaseApi):
    def get_user_info(self, token):
        """
        获取用户信息
        :param token:
        :return:
        """
        self.token = token
        data = {
            "method": "get",
            "url": "/fmea/user/info"
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        user_info = json.loads(res.json()["data"])
        return user_info
