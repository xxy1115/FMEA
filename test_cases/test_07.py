# -*- coding: UTF-8 -*-
import os

import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from libs.CR.cr_change_status import crChangeStatus
from libs.CR.cr_export import crExport
from libs.CR.cr_feature_update import crFeatureUpdate
from libs.CR.cr_function_update import crFunctionUpdate
from libs.CR.cr_invalid_update import crInvalidUpdate
from libs.CR.cr_product_update import crProductUpdate
from libs.CR.cr_publish import crPublish
from libs.CR.get_default_customer import getDefaultCustomer
from libs.CR.select_up_product import selectUpProduct
from libs.dfmea.delete_dfmea import deleteDfmea
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.exteral_IF_update import exteralIFUpdate
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    """客户要求"""
    token = ""
    user_id = 1681
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    product_types = []  # 产品类别
    added_product_nodes = []  # 添加的产品节点

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_04.yaml")
        crExport().del_last_export()  # 删除上次导出的客户要求

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

    @allure.title("客户要求-添加外部界面关系")
    def test_5(self):
        if_type_list = TestCase1.dicts["009"]
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:添加外部界面关系"):
            res = exteralIFUpdate().add_exteral_IF(TestCase1.token, if_type_list, TestCase1.product_type,
                                                   project_serial, 1)
            pytest.assume(res["flag"], "添加外部界面关系失败")
        with allure.step("step2:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "selectUpProduct失败")
            pif_serial = res["list"][0]["pifSerial"]
        with allure.step("step3:saveOrUpdateCustomerRequestChangeStatus"):
            res = crChangeStatus().cr_change_status1(TestCase1.token, project_serial)
            pytest.assume(res["flag"], "saveOrUpdateCustomerRequestChangeStatus失败")
        with allure.step("step4:客户要求导出"):
            crExport().cr_export(TestCase1.token, project_serial, "客户要求-客户界面.xls")
            pytest.assume(os.path.exists("customer_request/客户要求-客户界面.xls"), "导出失败")
        with allure.step("step5:删除外部界面关系"):
            res = exteralIFUpdate().del_exteral_IF(TestCase1.token, pif_serial)
            pytest.assume(res, "删除外部界面关系失败")
        with allure.step("step6:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "selectUpProduct失败")

    @allure.title("客户要求-添加上级产品")
    def test_6(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:添加上级产品"):
            res = crProductUpdate().add_cr_product(TestCase1.token, TestCase1.product_type, project_serial)
            pytest.assume(res["flag"], "添加上级产品失败")
            TestCase1.ppt_serial = res["pptSerial"]
        with allure.step("step2:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "失败")
        # with allure.step("step3:saveOrUpdateCustomerRequestChangeStatus"):
        #     res = crChangeStatus().cr_change_status1(TestCase1.token, project_serial)
        #     pytest.assume(res["flag"], "客户要求发布失败")

    @allure.title("客户要求-添加上级产品功能")
    def test_7(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:获取默认客户"):
            res = getDefaultCustomer().get_default_customer(TestCase1.token, project_serial)
            pytest.assume(res, "获取默认客户失败")
            TestCase1.default_customer = res["customer"]
        with allure.step("step2:上级要求中添加产品功能"):
            # 未使用默认客户过滤，防止过滤后取不到数据
            res = crFunctionUpdate().add_cr_function(TestCase1.token, TestCase1.product_type, TestCase1.ppt_serial, 2)
            pytest.assume(res["flag"], "添加上级产品功能失败")
            TestCase1.add_up_fun_nodes = res["projectFunctions"]
        with allure.step("step3:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "失败")

    @allure.title("客户要求-添加上级特性")
    def test_8(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:上级要求中添加产品特性"):
            pf_serial = TestCase1.add_up_fun_nodes[0]["serialNum"]
            res = crFeatureUpdate().add_cr_feature(TestCase1.token, TestCase1.product_type, pf_serial, 2)
            pytest.assume(res, "添加上级特性失败")
            TestCase1.add_up_feature_nodes = res
        with allure.step("step2:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "失败")

    @allure.title("客户要求-添加上级失效")
    def test_9(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        with allure.step("step1:上级要求中添加失效"):
            pfe_serial = TestCase1.add_up_feature_nodes[0]["serialNum"]
            res = crInvalidUpdate().add_cr_invalid(TestCase1.token, TestCase1.product_type, pfe_serial,
                                                   TestCase1.ppt_serial, 2)
            pytest.assume(res["flag"], "添加上级失效失败")
            TestCase1.add_up_invalid_nodes = res["projectInvalids"]
        with allure.step("step2:selectUpProduct"):
            res = selectUpProduct().select_up_product(TestCase1.token, project_serial)
            pytest.assume(res, "失败")
            TestCase1.change_serial = res["changeStatus"]["serialNum"]

    @allure.title("客户要求导出")
    def test_10(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        crExport().cr_export(TestCase1.token, project_serial, "客户要求-上级要求.xls")
        pytest.assume(os.path.exists("customer_request/客户要求-上级要求.xls"), "导出失败")

    @allure.title("客户要求-发布")
    def test_11(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = crPublish().cr_publish(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "客户要求发布失败")

    @allure.title("客户要求-更改状态")
    def test_12(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = crChangeStatus().cr_change_status(TestCase1.token, TestCase1.user_id, project_serial,
                                                TestCase1.change_serial)
        pytest.assume(res["flag"], "更改状态失败")

    # @allure.title("结构树-根节点添加功能")
    # def test_12(self):
    #     ppt_serial = TestCase1.dfmea_info["project"]["pptSerial"]  # 在根节点添加功能
    #     res = functionNodesUpdate().add_function_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, 1)
    #     pytest.assume(res, "添加功能失败")
    #     TestCase1.added_function_nodes = res
    #
    # @allure.title("结构树-根节点添加失效")
    # def test_13(self):
    #     ppt_serial = TestCase1.dfmea_info["project"]["pptSerial"]
    #     pf_serial = TestCase1.added_function_nodes[0]["serialNum"]  # 父级功能节点
    #     res = invalidNodesUpdate().add_invalid_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, pf_serial, 1)
    #     pytest.assume(res, "添加失效失败")
    #     TestCase1.added_invalid_nodes = res

    @allure.title("客户要求-删除产品")
    def test_13(self):
        res = crProductUpdate().del_cr_product(TestCase1.token, TestCase1.ppt_serial)
        pytest.assume(res["flag"] == "1", "删除产品失败")

    @allure.title("删除DFMEA")
    def test_14(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = deleteDfmea().delete_dfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除DFMEA失败")
