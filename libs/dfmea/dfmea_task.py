# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_max_num import getMaxNum


class DfmeaTask(BaseApi):
    def dfmea_task(self, token, user_id, project, role_type):
        self.token = token
        task_num = getMaxNum().get_max_num(token, "project_task", "task_num", "PR")
        # task_num = self.get_max_num()
        data = {
            "method": "post",
            "url": "/gateway/fmea-system/projectTask/saveOrUpdate",
            "json": {
                "deliverable": project["deliverable"],
                "planEndDate": project["enddate"],
                "planStartDate": project["startdate"],
                "pptSerial": project["pptSerial"],
                "projectId": project["projectId"],
                "projectTaskMembers": [{
                    "userId": user_id,
                    "userRole": role_type
                }],
                "taskNum": task_num
            }
        }
        res = self.send(data)
        if res.status_code != 200:
            return False
        if res.json()["meta"] and res.json()["meta"]["success"] != True:
            return False
        result = json.loads(res.json()["data"])
        return [result["flag"], task_num]
