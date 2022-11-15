# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.pfmea_tree import PfmeaTree
from libs.pfmea.add_pfmea import addPFMEA
from libs.pfmea.add_pfmea_template import addPFMEATemplate
from libs.pfmea.delete_pfmea import deletePFMEA
from libs.pfmea.pfmea_list import PfmeaList
from libs.pfmea.pfmea_share import PfmeaShare
from libs.pfmea.pfmea_task import PfmeaTask
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 0
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    pfmea_info = {}  # 创建PFMEA返回信息
    added_procedures_nodes = []

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_06.yaml")

    def teardown_class(self):
        pass

    @allure.title("登录")
    def test_1(self):
        res = Login().login(self.test_data["user"]["user01"])
        pytest.assume(res, "登录失败")
        TestCase1.token = res["token"]
        TestCase1.user_id = res["userId"]

    @allure.title("获取字典")
    def test_2(self):
        res = getDict().get_dict(TestCase1.token)
        pytest.assume(res, "字典接口失败")
        TestCase1.dicts = res

    @allure.title("获取用户信息")
    def test_3(self):
        res = getUserInfo().get_user_info(TestCase1.token)
        pytest.assume(res, "用户信息接口失败")
        TestCase1.user_info = res
        TestCase1.product_type = res["productTypePermissionList"]

    @allure.title("新建PFMEA")
    def test_4(self):
        procedureName = TestCase1.dicts["042"][1]["name"]
        enProcedureName = TestCase1.dicts["042"][1]["enName"]
        customer = TestCase1.dicts["006"][0]["code"]  # 006客户
        secrecyGrade = TestCase1.dicts["011"][0]["code"]  # 011客户
        with allure.step("step1:选择项目"):
            res = programList().program_list(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            program_obj = res[0]
        with allure.step("step2:获取产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            product = res[0]
        with allure.step("step3:获取关联产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            related_product = res[2]
        with allure.step("step4:新建PFMEA"):
            res = addPFMEA().add_pfmea(self.test_data["project"], TestCase1.token, TestCase1.user_id,
                                       self.test_data["user"]["user01"][0], product, related_product, program_obj,
                                       procedureName, enProcedureName, customer, secrecyGrade)
            pytest.assume(res, "新建PFMEA失败")
            TestCase1.pfmea_info = res
        with allure.step("step5:创建任务"):
            projectProcedureSerial = TestCase1.pfmea_info["projectProcedure"]["serialNum"]
            pfmeaProject = TestCase1.pfmea_info["pfmeaProject"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = PfmeaTask().pfmea_task(TestCase1.token, TestCase1.user_id, role_type,
                                                    projectProcedureSerial, pfmeaProject)
            pytest.assume(flag, "创建PFMEA任务失败")
            TestCase1.project_task_num = task_num

    @allure.title("获取PFMEA结构树")
    def test_5(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        res = PfmeaTree().pfmea_tree(TestCase1.token, project_serial)
        pytest.assume(res, "获取PFMEA结构树失败")
        pytest.assume(res["data"]["pppSerial"] == TestCase1.pfmea_info["projectProcedure"]["serialNum"],
                      "结构树根节点serialNum错误")

    @allure.title("PFMEA共享")
    def test_6(self):
        project_id = TestCase1.pfmea_info["pfmeaProject"]["projectId"]
        project_serial = TestCase1.pfmea_info["pfmeaProject"]["serialNum"]
        with allure.step("step1:全部共享"):
            res = PfmeaShare().pfmea_share_all(TestCase1.token, project_id, project_serial)
            pytest.assume(res["flag"], "PFMEA共享失败")
        with allure.step("step2:部分共享"):
            res = PfmeaShare().pfmea_share_part(TestCase1.token, project_id, project_serial, TestCase1.user_id,
                                                self.test_data["user"]["user01"][0])
            pytest.assume(res["flag"], "PFMEA共享失败")

    @allure.title("我的PFMEA列表查询")
    def test_7(self):
        project_num = TestCase1.pfmea_info["pfmeaProject"]["projectNum"]
        res = PfmeaList().my_pfmea_list(TestCase1.token, TestCase1.user_id, project_num)
        pytest.assume(res, "我的PFMEA列表查询失败")
        pytest.assume(len(res) > 0, "我的PFMEA列表数据空")
        pytest.assume(res[0]["productName"] == TestCase1.pfmea_info["pfmeaProject"]["productName"], "产品名称错误")

    @allure.title("共享PFMEA列表查询")
    def test_8(self):
        project_num = TestCase1.pfmea_info["pfmeaProject"]["projectNum"]
        res = PfmeaList().share_pfmea_list(TestCase1.token, TestCase1.user_id, project_num)
        pytest.assume(res, "共享PFMEA列表查询失败")
        pytest.assume(len(res) > 0, "共享PFMEA列表数据空")
        pytest.assume(res[0]["product"]["productName"] == TestCase1.pfmea_info["pfmeaProject"]["productName"], "产品名称错误")

    @allure.title("全部PFMEA列表查询")
    def test_9(self):
        project_num = TestCase1.pfmea_info["pfmeaProject"]["projectNum"]
        res = PfmeaList().all_pfmea_list(TestCase1.token, TestCase1.product_type, project_num)
        pytest.assume(res, "全部PFMEA列表失败")
        pytest.assume(len(res) > 0, "全部PFMEA列表数据空")
        pytest.assume(res[0]["productName"] == TestCase1.pfmea_info["pfmeaProject"]["productName"], "产品名称错误")

    @allure.title("创建基础FMEA")
    def test_10(self):
        procedureName = TestCase1.dicts["042"][1]["name"]
        enProcedureName = TestCase1.dicts["042"][1]["enName"]
        customer = TestCase1.dicts["006"][0]["code"]  # 006客户
        secrecyGrade = TestCase1.dicts["011"][0]["code"]  # 011客户
        with allure.step("step1:选择项目"):
            res = programList().program_list(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            program_obj = res[1]
        with allure.step("step2:获取产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            product = res[1]
        with allure.step("step3:获取关联产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            related_product = res[2]
        with allure.step("step4:新建PFMEA"):
            res = addPFMEATemplate().add_pfmea_template(self.test_data["project_template"], TestCase1.token, TestCase1.user_id,
                                       self.test_data["user"]["user01"][0], product, related_product, program_obj,
                                       procedureName, enProcedureName, customer, secrecyGrade)
            pytest.assume(res, "新建PFMEA失败")
            TestCase1.pfmea_template_info = res
        with allure.step("step5:保存模板"):
            ppt_serial = TestCase1.pfmea_template_info["projectProcedure"]["serialNum"]
            project_serial = TestCase1.pfmea_template_info["projectProcedure"]["projectSerial"]
            project_name = TestCase1.pfmea_template_info["pfmeaProject"]["projectName"]
            procedure_name = TestCase1.pfmea_template_info["pfmeaProject"]["procedureName"]
            res = addPFMEATemplate().save_template(TestCase1.token, ppt_serial, project_serial, project_name, procedure_name)
            pytest.assume(res["flag"] == 1, "保存模板失败")
        with allure.step("step6:创建任务"):
            projectProcedureSerial = TestCase1.pfmea_template_info["projectProcedure"]["serialNum"]
            pfmeaProject = TestCase1.pfmea_template_info["pfmeaProject"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = PfmeaTask().pfmea_task(TestCase1.token, TestCase1.user_id, role_type,
                                                    projectProcedureSerial, pfmeaProject)
            pytest.assume(flag, "创建PFMEA任务失败")
            TestCase1.template_task_num = task_num

    @allure.title("基础PFMEA列表查询")
    def test_11(self):
        project_num = TestCase1.pfmea_template_info["pfmeaProject"]["projectNum"]
        res = PfmeaList().template_pfmea_list(TestCase1.token, TestCase1.user_id, TestCase1.product_type, project_num)
        pytest.assume(res, "基础PFMEA列表失败")
        pytest.assume(len(res) > 0, "基础PFMEA列表数据空")
        pytest.assume(res[0]["productNum"] == TestCase1.pfmea_template_info["pfmeaProject"]["productNum"], "产品编号错误")
        TestCase1.template_serial_num = res[0]["serialNum"]

    @allure.title("删除基础PFMEA")
    def test_12(self):
        res = deletePFMEA().delete_template_pfmea(TestCase1.token, TestCase1.template_serial_num)
        pytest.assume(res["flag"], "删除基础PFMEA失败")

    @allure.title("删除PFMEA")
    def test_13(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        res = deletePFMEA().delete_pfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除PFMEA失败")
