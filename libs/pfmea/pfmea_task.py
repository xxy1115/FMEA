# -*- coding: UTF-8 -*-
import json

from common.base import BaseApi
from common.get_max_num import getMaxNum


class PfmeaTask(BaseApi):
    def pfmea_task(self, token, user_id, role_type, projectProcedureSerial, project):
        self.token = token
        task_num = getMaxNum().get_max_num(token, "pfmea_project_procedure_task", "task_num", "PT")
        data = {
            "method": "post",
            "url": "/pfmea_end/pfmeaProjectTask/saveOrUpdate",
            "json": {
                "deliverable": project["deliverable"],
                "isApproval": "1",
                "planEndDate": project["enddate"],
                "planStartDate": project["startdate"],
                "projectId": project["projectId"],
                "projectProcedureSerial": projectProcedureSerial,
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
        result = res.json()["data"]
        return [result["flag"], task_num]
