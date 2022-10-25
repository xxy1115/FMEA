# -*- coding: UTF-8 -*-
import json
import time

import requests

from common.base import BaseApi
from configs.config import HOST
from utils.encrypt_md5 import get_md5


class Login(BaseApi):
    def login(self, data):
        """
        登录
        :param data: 用户名,密码
        :return: [token,用户ID]
        """
        url = f'{HOST}/gateway/fmea-system/login'
        timestamp = int(round(time.time() * 1000))
        username = data[0]
        password = get_md5(data[1])  # 调用md5加密方法
        data = {
            "timestamp": timestamp,
            "username": username,
            "password": password,
            "adPassword": "",
            "forceLogin": True
        }
        r = requests.post(url, data=data)
        if r.status_code != 200:
            return False
        user_data = json.loads(r.json()["data"])
        self.token = user_data["token"]
        return user_data
