# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.dfmea_tree import DfmeaTree
from libs.dfmea.pfmea_tree import PfmeaTree
from libs.pfmea.add_pfmea import addPFMEA
from libs.pfmea.pfmea_task import PfmeaTask
from libs.pfmea.procedure_nodes_update import procedureNodesUpdate
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
        self.test_data = parse_yaml("../data/data_08.yaml")

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

    @allure.title("结构树添加工序节点")
    def test_6(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        ppp_serial = TestCase1.pfmea_info["projectProcedure"]["serialNum"]
        res = procedureNodesUpdate().add_procedure_nodes(TestCase1.token, TestCase1.product_type, project_serial,
                                                         ppp_serial, 3)
        pytest.assume(res["flag"], "添加工序节点失败")
        TestCase1.added_procedures_nodes = res["pfmeaProjectProcedures"]

    # @allure.title("结构树编辑产品节点")
    # def test_7(self):
    #     serial_num = TestCase1.added_product_nodes[0]["serialNum"]  # 编辑第一个产品节点
    #     res = productNodesUpdate().edit_product_nodes(self.test_data["edit_product_nodes"], TestCase1.token,
    #                                                   TestCase1.product_type,
    #                                                   serial_num)
    #     pytest.assume(res == 1, "编辑产品节点失败")
    #
    # @allure.title("结构树删除产品节点")
    # def test_8(self):
    #     serial_num = TestCase1.added_product_nodes[1]["serialNum"]  # 删除第二个产品节点
    #     res = productNodesUpdate().del_product_nodes(TestCase1.token, serial_num)
    #     pytest.assume(res["flag"] == "1", "删除产品节点失败")
    #
    # @allure.title("结构树添加功能节点")
    # def test_9(self):
    #     ppt_serial = TestCase1.added_product_nodes[2]["serialNum"]  # 在第三个产品节点添加功能
    #     res = functionNodesUpdate().add_function_nodes(self.test_data["add_function_nodes"], TestCase1.token,
    #                                                    TestCase1.product_type, ppt_serial)
    #     pytest.assume(res, "添加功能节点失败")
    #     TestCase1.added_function_nodes = res
    #
    # @allure.title("结构树编辑功能节点")
    # def test_10(self):
    #     project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
    #     serial_num = TestCase1.added_function_nodes[0]["serialNum"]  # 编辑第一个功能节点
    #     res = functionNodesUpdate().edit_function_nodes(self.test_data["edit_function_nodes"], TestCase1.token,
    #                                                     TestCase1.product_type, project_serial, serial_num)
    #     pytest.assume(res == 1, "编辑功能节点失败")
