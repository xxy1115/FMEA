# -*- coding: UTF-8 -*-
import random

from common.base import BaseApi
from common.get_product import getProduct


class saveBomVersion(BaseApi):
    def save_bom_version_for_list(self, token, product_type, bom_serial, product_id, serial_num, site_id):
        """
        BOM清单保存
        :param token:
        :param serial_num:
        :return:
        """
        self.token = token
        products = getProduct().get_product(token, product_type)
        product = products[3]  # 取产品库中第4个产品
        # 生成32位随机数
        num = []
        for n in range(32):
            num.append(random.choice("1234567890abcdef"))
        children_serialNum = "".join(num)
        data = {
            "method": "post",
            "url": "/gateway/fmea-maindata/bom/saveNewBomVersionForList",
            "json": {
                "bomSerial": bom_serial,
                "children": [{
                    "bomSerial": bom_serial,
                    "children": [],
                    "count": "",
                    "parentId": serial_num,
                    "productId": product["productId"],
                    "remark": "",
                    "serialNum": children_serialNum
                }],
                "count": "",
                "orgId": "",
                "parentId": "-1",
                "productId": product_id,
                "remark": "",
                "serialNum": serial_num,
                "siteId": site_id,
                "standby1": "",
                "standby2": "",
                "standby3": "",
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = res.json()["data"]
        return result
