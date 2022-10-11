# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.kt import KT
from libs.dfmea.product_nodes_update import productNodesUpdate
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 1681
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    product_types = []  # 产品类别
    added_product_nodes = []  # 添加的产品节点

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_02.yaml")

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
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
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

    @allure.title("结构树添加产品节点")
    def test_5(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        product_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        res = productNodesUpdate().add_product_nodes(TestCase1.token, TestCase1.product_type, project_serial,
                                                     product_serial, 3)
        pytest.assume(res, "添加产品节点失败")
        TestCase1.added_product_nodes = res

    @allure.title("框图获取新节点")
    def test_6(self):
        ppt_serials1 = TestCase1.added_product_nodes[0]["serialNum"]
        ppt_serials2 = TestCase1.added_product_nodes[1]["serialNum"]
        ppt_serials3 = TestCase1.added_product_nodes[2]["serialNum"]
        ppt_serials = [ppt_serials1, ppt_serials2, ppt_serials3]
        res = KT().get_all_Kt_new(TestCase1.token, ppt_serials)
        pytest.assume(res["flag"], "接口返回错误")
        pytest.assume(len(res["list"]) == 3, "获取节点数量不对")

    @allure.title("框图获取当前所有节点")
    def test_7(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        res = KT().get_kt(TestCase1.token, project_serial)
        pytest.assume(res, "框图获取当前所有节点失败")
        TestCase1.kt_info = res

    @allure.title("框图编辑保存")
    def test_8(self):
        ppt_serial = TestCase1.kt_info["kt"]["pptSerial"]
        project_serial = TestCase1.kt_info["kt"]["projectSerial"]
        kt_serial = TestCase1.kt_info["kt"]["serialNum"]
        ktNodeList = TestCase1.kt_info["ktNodeList"]
        ktNodes = [TestCase1.added_product_nodes[0], TestCase1.added_product_nodes[1]]
        res = KT().save_kt_data(TestCase1.token, ppt_serial, project_serial, kt_serial, ktNodeList, ktNodes)
        pytest.assume(res["flag"] == "1", "框图编辑保存失败")

    @allure.title("保存连线类型")
    def test_9(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        res = KT().save_line_type(TestCase1.token, ppt_serial, project_serial)
        pytest.assume(res, "保存连线类型失败")
