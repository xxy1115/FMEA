# -*- coding: UTF-8 -*-
import json
import time
import requests
from configs.config import HOST
from utils.encrypt_md5 import get_md5


class BaseApi:
    token = ""

    def send(self, data):
        """
        接口调用
        :param data: 请求信息
        :return: 响应体
        """
        if "http:" not in data["url"]:  # url拼接后直接改变了yaml数据，再次使用不需要拼接
            data["url"] = HOST + data["url"]
        if "params" not in data:
            data["params"] = {}
        data["params"]["timestamp"] = int(round(time.time() * 1000))
        data["headers"] = {"X-Token": self.token}
        r = requests.request(**data)
        print('-------------base--------------')
        # print(r.json())
        return r

    def get_token(self, data):  # 弃用
        """
        获取token
        :param data: 用户名密码
        :return: [token,用户ID]
        """
        url = HOST + "/gateway/fmea-system/login"
        timestamp = int(round(time.time() * 1000))
        username = data["username"]
        password = get_md5(data["password"])  # 调用md5加密方法
        data = {
            "timestamp": timestamp,
            "username": username,
            "password": password,
            "adPassword": "",
            "forceLogin": True
        }
        r = requests.post(url, data=data)
        user_data = json.loads(r.json()["data"])
        self.token = user_data["token"]
        return user_data
