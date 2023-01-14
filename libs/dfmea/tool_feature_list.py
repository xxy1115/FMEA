# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi


class toolFeatureList(BaseApi):
    def publish_kcds(self, token, ppt_serial, features):
        self.token = token
        kcdsItems = []
        for index, item in enumerate(features):
            kcdsItems.append({
                "controlFeature": item["controlFeature"],
                "det": "",
                "enProductFeature": item["enFeature"],  # 系统中没有英文名的情况下传中文名
                "featureCategorySerial": "",
                "featureSerial": item["productFeatureSerial"],
                "number": index + 1,
                "occurence": "",
                "pfeSerial": item["serialNum"],
                "pidSerial": "",
                "productFeature": item["feature"],
                "remark": "",
                "serialNum": "",
                "severity": "--",
                "technicalRequirements": item["technicalRequirements"]
            })
        data = {
            "method": "post",
            "url": "/gateway/fmea-dfmea/kcds/publishKcds",
            "json": {
                "kcdsItems": kcdsItems,
                "lanTuMessageType": "0",
                "pptSerial": ppt_serial,
                "programId": "",
                "remark": "发布",
                "serialNum": "",
                "status": "",
                "versionNo": 0
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        result = res.json()["data"]
        return result
