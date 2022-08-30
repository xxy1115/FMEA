# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from libs.dfmea.dfmea_list import DfmeaList
from libs.dfmea.dfmea_task import DfmeaTask
from libs.program_add import addProgram
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = ""
    dicts = {}
    program_serial = ""
    program_num = ""  # 项目编号
    user_info = {}
    dfmea_info = {}
    project_task_num = ""  # DFMEA任务编号

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_01.yaml")

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
        print("获取字典：", res)

    @allure.title("获取用户信息")
    def test_3(self):
        res = getUserInfo().get_user_info(TestCase1.token)
        TestCase1.user_info = res
        pytest.assume(res, "用户信息接口失败")

    @allure.title("新建项目")
    def test_4(self):
        product_type = TestCase1.user_info["productTypePermissionList"]
        with allure.step("step1:获取产品信息"):
            product_num = self.test_data["program"]["api"]["json"]["productNum"]
            res = getProduct().get_product(TestCase1.token, product_type, product_num)
            pytest.assume(res, "产品信息接口失败")
            pytest.assume(res[0]["productNum"] == product_num, "产品查询结果错误")
            product = res[0]
        with allure.step("step2:新建项目"):
            res = addProgram().add_program(self.test_data["program"], product, TestCase1.token,
                                           TestCase1.user_id,
                                           TestCase1.dicts["010"], TestCase1.dicts["001"])  # 010-车型,001-平台
            pytest.assume(res, "新建项目失败")
            TestCase1.program_serial, TestCase1.program_num = res  # 项目序列号、项目编号存入类变量
        with allure.step("step3:项目列表查询"):
            res = programList().program_list(TestCase1.token, product_type, TestCase1.program_num)
            pytest.assume(res, "项目列表查询接口错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            pytest.assume(res[0]["programNum"] == TestCase1.program_num, "项目列表查询结果错误")
            pytest.assume(res[0]["dfmeaCount"] == 0, "DFMEA数量错误")
            pytest.assume(res[0]["pfmeaCount"] == 0, "PFMEA数量错误")

    @allure.title("新建DFMEA")
    def test_5(self):
        product_type = TestCase1.user_info["productTypePermissionList"]
        with allure.step("step1:获取产品信息"):
            product_num = self.test_data["project"]["api"]["json"]["productNum"]
            res = getProduct().get_product(TestCase1.token, product_type, product_num)
            pytest.assume(res, "产品信息接口失败")
            pytest.assume(res[0]["productNum"] == product_num, "产品查询结果错误")
            product = res[0]
        with allure.step("step2:选择项目"):
            res = programList().program_list(TestCase1.token, product_type,
                                             TestCase1.program_num)
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            program_obj = res[0]
            pytest.assume(program_obj["programNum"] == TestCase1.program_num, "项目列表查询结果错误")
        with allure.step("step3:新建DFMEA"):
            res = addDFMEA().add_dfmea(self.test_data["project"], product, program_obj, TestCase1.token,
                                       TestCase1.user_id,
                                       self.test_data["user"]["user01"][0],
                                       TestCase1.dicts["001"], TestCase1.dicts["006"],
                                       TestCase1.dicts["011"], TestCase1.dicts["049"])  # 001平台 006客户 011保密等级 049模块
            pytest.assume(res, "新建DFMEA失败")
            TestCase1.dfmea_info = res
        with allure.step("step4:创建任务"):
            project = TestCase1.dfmea_info["project"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = DfmeaTask().dfmea_task(TestCase1.token, TestCase1.user_id,
                                                      project, role_type)
            pytest.assume(flag, "创建DFMEA任务失败")
            TestCase1.project_task_num = task_num  # 获取任务编号DFMEA新建任务使用
            print(task_num)
        with allure.step("step5:我的FMEA列表查询"):
            res = DfmeaList().dfmea_list(self.test_data["project_list"], TestCase1.token, TestCase1.user_id, role_type,
                                         project["projectNum"])
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(res[0]["projectNum"] == project["projectNum"], "FMEA编号查询结果错误")
            pytest.assume(res[0]["projectName"] == project["projectName"], "FMEA名称查询结果错误")
            # print(json.dumps(res.json()["data"], indent=2))
