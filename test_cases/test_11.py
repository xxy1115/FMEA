# -*- coding: UTF-8 -*-
import os

import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.add_dfmea import addDFMEA
from libs.dfmea.delete_dfmea import deleteDfmea
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.feature_nodes_update import featureNodesUpdate
from libs.dfmea.tool_feature_list import toolFeatureList
from libs.pfmea.add_pfmea import addPFMEA
from libs.pfmea.delete_pfmea import deletePFMEA
from libs.pfmea.export_feature import exportFeature
from libs.pfmea.import_feature import importFeature
from libs.pfmea.pfmea_task import PfmeaTask
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 0
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    pfmea_info = {}  # 创建PFMEA返回信息

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_02.yaml")
        self.test_data2 = parse_yaml("../data/data_05.yaml")

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

    @allure.title("添加根节点的特性")
    def test_5(self):
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]  # 获取根节点serialNum
        res = featureNodesUpdate().add_feature_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, 3)
        pytest.assume(res, "添加特性节点失败")
        TestCase1.added_feature_nodes = res

    @allure.title("特性清单发布")
    def test_6(self):
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]  # 获取根节点serialNum
        res = toolFeatureList().publish_kcds(TestCase1.token, ppt_serial, TestCase1.added_feature_nodes)
        pytest.assume(res["flag"], "特性清单发布失败")

    @allure.title("新建PFMEA")
    def test_7(self):
        product_num = TestCase1.dfmea_info["project"]["productNum"]
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
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type, product_num)
            pytest.assume(res, "产品信息接口失败")
            product = res[0]
        with allure.step("step3:获取关联产品信息"):
            res = getProduct().get_product(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "产品信息接口失败")
            related_product = res[2]
        with allure.step("step4:新建PFMEA"):
            res = addPFMEA().add_pfmea(self.test_data2["project"], TestCase1.token, TestCase1.user_id,
                                       self.test_data2["user"]["user01"][0], product, related_product, program_obj,
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

    @allure.title("加载特性列表")
    def test_8(self):
        product_id = TestCase1.pfmea_info["pfmeaProject"]["productId"]
        with allure.step("step1:DFMEA项目特性列表"):
            res1 = importFeature().dfmeaFeatureList(TestCase1.token, TestCase1.product_type, product_id)
            pytest.assume(len(res1) > 0, "DFMEA项目特性列表为空")
            TestCase1.feature_dfmea_list1 = res1
        with allure.step("step2:产品归档特性列表"):
            res2 = importFeature().dfmeaFeatureProductIdList(TestCase1.token, TestCase1.product_type, product_id)
            pytest.assume(len(res1) > 0, "产品归档特性列表为空")
            TestCase1.feature_dfmea_list2 = res2

    @allure.title("保存特性列表")
    def test_9(self):
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]  # 获取DFMEA根节点serialNum
        pfmea_project_serial = TestCase1.pfmea_info["pfmeaProject"]["serialNum"]
        product_id = TestCase1.pfmea_info["pfmeaProject"]["productId"]
        with allure.step("step1:保存特性列表"):
            res = importFeature().saveImportFeature(TestCase1.token, pfmea_project_serial, ppt_serial, product_id,
                                                    TestCase1.added_feature_nodes)
            pytest.assume(res["flag"], "保存特性列表失败")
        with allure.step("step2:selectPfmeaProductFeatureList"):
            project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
            res = importFeature().selectPfmeaProductFeatureList(TestCase1.token, project_serial)
            pytest.assume(res, "selectPfmeaProductFeatureList接口失败")

    @allure.title("导入Excel")
    def test_10(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        res = importFeature().import_excel(TestCase1.token, project_serial)
        pytest.assume(res["data"] == "success", "导入Excel失败")

    @allure.title("导出产品特性")
    def test_11(self):
        exportFeature().del_last_file()  # 删除上次导出的产品特性
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        file_name = exportFeature().export_feature(TestCase1.token, project_serial)
        pytest.assume(os.path.exists(f"pfmea_feature/{file_name}"), "导出失败")
        report = os.stat(f"pfmea_feature/{file_name}")
        pytest.assume(report.st_size > 0, "导出文件大小为0")

    @allure.title("存档")
    def test_12(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        with allure.step("step1:存档"):
            res = importFeature().archiveProductFeature(TestCase1.token, project_serial)
            pytest.assume(res["flag"], "存档失败")
        with allure.step("step2:获取版本列表"):
            res = importFeature().getProductFeatureVersionList(TestCase1.token, project_serial)
            pytest.assume(res["productFeatureVersionList"], "获取版本列表失败")
            pytest.assume(len(res["productFeatureVersionList"]) > 0, "版本列表为空")
        with allure.step("step3:selectPfmeaProductFeatureList"):
            res = importFeature().selectPfmeaProductFeatureList(TestCase1.token, project_serial)
            pytest.assume(res, "selectPfmeaProductFeatureList接口失败")
            pytest.assume(res["currentFeatureVersion"], "currentFeatureVersion为空")

    @allure.title("删除DFMEA")
    def test_13(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = deleteDfmea().delete_dfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除DFMEA失败")

    @allure.title("删除PFMEA")
    def test_14(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        res = deletePFMEA().delete_pfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除PFMEA失败")
