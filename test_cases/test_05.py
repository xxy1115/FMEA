# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from libs.dfmea.bom import BOM
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 0
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    dfmea_info2 = {}
    project_task_num = ""  # DFMEA任务编号
    product_types = []  # 产品类别
    bom_list = []

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_04.yaml")

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

    @allure.title("新建DFMEA")
    def test_4(self):
        with allure.step("step1:获取产品信息"):
            product_num = self.test_data["project"]["api"]["json"]["productNum"]
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type, product_num)
            pytest.assume(res, "产品信息接口失败")
            pytest.assume(res[0]["productNum"] == product_num, "产品查询结果错误")
            product = res[0]
        with allure.step("step2:选择项目"):
            res = programList().program_list(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            program_obj = res[0]
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

    @allure.title("判断DFMEA项目是否包含子零件")
    def test_5(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        flag = BOM().is_has_children(TestCase1.token, project_serial)
        pytest.assume(flag == "1", "包含子零件")

    @allure.title("加载BOM列表")
    def test_6(self):
        product_Id = TestCase1.dfmea_info["productTree"]["productId"]
        items = BOM().bom_list(TestCase1.token, product_Id)
        pytest.assume(items, "加载BOM列表失败")
        pytest.assume(len(items) > 0, "BOM列表数据空")
        TestCase1.bom_list = items

    @allure.title("导入BOM")
    def test_7(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        bom_serial = TestCase1.bom_list[3]["serialNum"]
        flag = BOM().import_bom(TestCase1.token, project_serial, bom_serial, ppt_serial)
        pytest.assume(flag, "导入BOM失败")

    @allure.title("通过项目编号获取BOM列表")
    def test_8(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        res = BOM().get_bom_list_by_serialNum(TestCase1.token, project_serial)
        pytest.assume(res, "获取BOM列表失败")
        pytest.assume(len(res) > 0, "获取BOM列表没有数据")

    @allure.title("新建DFMEA")
    def test_9(self):
        with allure.step("step1:获取产品信息"):
            product_num = self.test_data["project"]["api"]["json"]["productNum"]
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type, product_num)
            pytest.assume(res, "产品信息接口失败")
            pytest.assume(res[0]["productNum"] == product_num, "产品查询结果错误")
            product = res[0]
        with allure.step("step2:选择项目"):
            res = programList().program_list(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "项目列表查询错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            program_obj = res[0]
        with allure.step("step3:新建DFMEA"):
            res = addDFMEA().add_dfmea(self.test_data["project"], product, program_obj, TestCase1.token,
                                       TestCase1.user_id,
                                       self.test_data["user"]["user01"][0],
                                       TestCase1.dicts["001"], TestCase1.dicts["006"],
                                       TestCase1.dicts["011"], TestCase1.dicts["049"])  # 001平台 006客户 011保密等级 049模块
            pytest.assume(res, "新建DFMEA失败")
            TestCase1.dfmea_info2 = res
        with allure.step("step4:创建任务"):
            project = TestCase1.dfmea_info2["project"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = DfmeaTask().dfmea_task(TestCase1.token, TestCase1.user_id,
                                                    project, role_type)
            pytest.assume(flag, "创建DFMEA任务失败")


    @allure.title("导入Excel")
    def test_10(self):
        project_serial = TestCase1.dfmea_info2["productTree"]["projectSerial"]
        # project_serial = "36362ed1b514487182852ed072651dce"
        res = BOM().import_excel(TestCase1.token, project_serial)
        pytest.assume(res == "success", "Excel导入失败")
