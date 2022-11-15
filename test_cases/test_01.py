# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.sys_user_list import sysUserList
from libs.delete_program import deleteProgram
from libs.dfmea.add_dfmea_template import addDFMEATemplate
from libs.dfmea.delete_dfmea import deleteDfmea
from libs.dfmea.dfmea_share import DfmeaShare
from libs.select_program_by_Id import selectProgramById
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
    user_id = 0
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
        pytest.assume(res, "用户信息接口失败")
        TestCase1.user_info = res
        TestCase1.product_type = res["productTypePermissionList"]

    @allure.title("新建项目")
    def test_4(self):
        with allure.step("step1:获取产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            product = res[0]
        with allure.step("step2:新建项目"):
            res = addProgram().add_program(TestCase1.token, TestCase1.user_id, self.test_data["user"]["user01"][0],
                                           product, TestCase1.dicts["010"],
                                           TestCase1.dicts["001"])  # 010-车型,001-平台
            pytest.assume(res, "新建项目失败")
            TestCase1.program_serial, TestCase1.program_num = res  # 项目序列号、项目编号存入类变量
        with allure.step("step3:通过ID选择项目"):
            res = selectProgramById().select_program_by_Id(TestCase1.token, TestCase1.program_serial)
            pytest.assume(res, "通过ID选择项目失败")
            pytest.assume(res["program"]["programNum"] == TestCase1.program_num, "项目编号不一致")

        with allure.step("step4:项目列表查询"):
            res = programList().program_list(TestCase1.token, TestCase1.product_type, TestCase1.program_num)
            pytest.assume(res, "项目列表查询接口错误")
            pytest.assume(len(res) > 0, "项目列表查询结果为空")
            pytest.assume(res[0]["programNum"] == TestCase1.program_num, "项目列表查询结果错误")
            pytest.assume(res[0]["dfmeaCount"] == 0, "DFMEA数量错误")
            pytest.assume(res[0]["pfmeaCount"] == 0, "PFMEA数量错误")

    @allure.title("新建DFMEA")
    def test_5(self):
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
            pytest.assume(res["flag"], "新建DFMEA失败")
            TestCase1.dfmea_info = res
        with allure.step("step4:创建任务"):
            project = TestCase1.dfmea_info["project"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = DfmeaTask().dfmea_task(TestCase1.token, TestCase1.user_id,
                                                    project, role_type)
            pytest.assume(flag, "创建DFMEA任务失败")
            TestCase1.project_task_num = task_num  # 获取任务编号DFMEA新建任务使用
            print(task_num)
            # print(json.dumps(res.json()["data"], indent=2))

    @allure.title("DFMEA共享")
    def test_6(self):
        project_id = TestCase1.dfmea_info["project"]["projectId"]
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:全部共享"):
            res = DfmeaShare().dfmea_share_all(TestCase1.token, project_id, project_serial)
            pytest.assume(res["flag"], "DFMEA共享失败")
        with allure.step("step2:查询已共享用户"):
            res = DfmeaShare().selectProjectShareMember(TestCase1.token, project_id)
            pytest.assume(res, "查询共享用户失败")
        with allure.step("step3:查询用户"):
            res = sysUserList().sys_user_list(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "查询用户失败")
        with allure.step("step4:部分共享"):
            res = DfmeaShare().dfmea_share_part(TestCase1.token, project_id, project_serial, TestCase1.user_id,
                                                self.test_data["user"]["user01"][0])
            pytest.assume(res["flag"], "DFMEA共享失败")

    @allure.title("我的DFMEA列表查询")
    def test_7(self):
        project_num = TestCase1.dfmea_info["project"]["projectNum"]
        project_name = TestCase1.dfmea_info["project"]["projectName"]
        role_type = TestCase1.user_info["role"][0]["roleType"]
        res = DfmeaList().dfmea_list(TestCase1.token, TestCase1.user_id, role_type, project_num)
        pytest.assume(res, "我的DFMEA列表查询失败")
        pytest.assume(len(res) > 0, "我的DFMEA列表数据空")
        pytest.assume(res[0]["projectNum"] == project_num, "FMEA编号查询结果错误")
        pytest.assume(res[0]["projectName"] == project_name, "FMEA名称查询结果错误")
        pytest.assume(res[0]["productName"] == TestCase1.dfmea_info["project"]["productName"], "产品名称错误")

    @allure.title("共享DFMEA列表查询")
    def test_8(self):
        project_num = TestCase1.dfmea_info["project"]["projectNum"]
        res = DfmeaList().share_dfmea_list(TestCase1.token, TestCase1.user_id, project_num)
        pytest.assume(res, "共享DFMEA列表查询失败")
        pytest.assume(len(res) > 0, "共享DFMEA列表数据空")
        pytest.assume(res[0]["product"]["productName"] == TestCase1.dfmea_info["project"]["productName"], "产品名称错误")

    @allure.title("全部DFMEA列表查询")
    def test_9(self):
        project_num = TestCase1.dfmea_info["project"]["projectNum"]
        res = DfmeaList().all_dfmea_list(TestCase1.token, TestCase1.product_type, project_num)
        pytest.assume(res, "全部DFMEA列表接口失败")
        pytest.assume(len(res) > 0, "全部DFMEA列表数据空")
        pytest.assume(res[0]["productName"] == TestCase1.dfmea_info["project"]["productName"], "产品名称错误")

    @allure.title("新建基础DFMEA")
    def test_10(self):
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
            res = addDFMEATemplate().add_dfmea_template(self.test_data["project_template"], product, program_obj,
                                                        TestCase1.token,
                                                        TestCase1.user_id,
                                                        self.test_data["user"]["user01"][0],
                                                        TestCase1.dicts["001"], TestCase1.dicts["006"],
                                                        TestCase1.dicts["011"],
                                                        TestCase1.dicts["049"])  # 001平台 006客户 011保密等级 049模块
            pytest.assume(res["flag"], "新建基础DFMEA失败")
            TestCase1.dfmea_template_info = res
        with allure.step("step4:保存模板"):
            ppt_serial = TestCase1.dfmea_template_info["project"]["pptSerial"]
            product_id = TestCase1.dfmea_template_info["project"]["productId"]
            product_name = TestCase1.dfmea_template_info["project"]["productName"]
            project_name = TestCase1.dfmea_template_info["project"]["projectName"]
            project_serial = TestCase1.dfmea_template_info["project"]["serialNum"]
            res = addDFMEATemplate().save_template(TestCase1.token, ppt_serial, product_id, product_name, project_name,
                                                   project_serial)
            pytest.assume(res["flag"] == 1, "保存模板失败")
        with allure.step("step5:创建任务"):
            project = TestCase1.dfmea_info["project"]
            role_type = TestCase1.user_info["role"][0]["roleType"]
            flag, task_num = DfmeaTask().dfmea_task(TestCase1.token, TestCase1.user_id, project, role_type)
            pytest.assume(flag, "创建DFMEA任务失败")
            TestCase1.template_task_num = task_num  # 获取任务编号DFMEA新建任务使用
            print(task_num)

    @allure.title("基础DFMEA列表查询")
    def test_11(self):
        project_num = TestCase1.dfmea_template_info["project"]["projectNum"]
        res = DfmeaList().template_dfmea_list(TestCase1.token, TestCase1.user_id, TestCase1.product_type,
                                              project_num)
        pytest.assume(res, "基础DFMEA列表失败")
        pytest.assume(len(res) > 0, "基础DFMEA列表数据空")
        pytest.assume(res[0]["productNum"] == TestCase1.dfmea_template_info["project"]["productNum"],
                      "产品编号错误")
        TestCase1.template_serial_num = res[0]["serialNum"]

    @allure.title("删除基础DFMEA")
    def test_12(self):
        res = deleteDfmea().delete_template_dfmea(TestCase1.token, TestCase1.template_serial_num)
        pytest.assume(res["flag"], "删除基础DFMEA失败")

    @allure.title("删除DFMEA")
    def test_13(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = deleteDfmea().delete_dfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除DFMEA失败")

    @allure.title("删除项目")
    def test_14(self):
        res = deleteProgram().delete_program(TestCase1.token, TestCase1.program_serial)
        pytest.assume(res["flag"], "删除项目失败")
