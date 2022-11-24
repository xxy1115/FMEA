# -*- coding: UTF-8 -*-
import os

import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.select_invalid_reason import selectInvalidReasonList
from common.select_invalid_result import selectInvalidResultList
from libs.dfmea.batch_invalid_net_update import batchInvalidNetUpdate
from libs.dfmea.delete_dfmea import deleteDfmea
from libs.dfmea.export_report import exportReport
from libs.dfmea.function_nodes_update import functionNodesUpdate
from libs.dfmea.invalid_nodes_update import invalidNodesUpdate
from libs.dfmea.product_nodes_update import productNodesUpdate
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.dfmea_tree import DfmeaTree
from libs.dfmea.save_invalid_nets import saveInvalidNets
from libs.dfmea.save_pf_relation import savePfRelation
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 0
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    project_task_num = ""  # DFMEA任务编号
    added_function1_nodes = []  # 根节点下的功能节点
    added_invalid1_nodes = []  # 根节点下的失效节点
    added_product2_nodes = []  # 添加的二级产品节点
    added_function2_nodes = []  # 二级产品的功能节点
    added_invalid2_nodes = []  # 二级产品的失效节点
    added_product3_nodes = []  # 添加的三级产品节点
    added_function3_nodes = []  # 三级产品的功能节点
    added_invalid3_nodes = []  # 三级产品的失效节点

    def setup_class(self):
        self.test_data = parse_yaml("../data/data_03.yaml")

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
            # print(json.dumps(res.json()["data"], indent=2))

    @allure.title("获取DFMEA结构树")
    def test_5(self):
        serial_num = TestCase1.dfmea_info["project"]["serialNum"]
        res = DfmeaTree().dfmea_tree(TestCase1.token, serial_num)
        pytest.assume(res, "获取DFMEA结构树失败")
        pytest.assume(res["data"]["text"] == TestCase1.dfmea_info["project"]["productName"], "结构树根节点产品名称错误")
        pytest.assume(res["data"]["pptSerial"] == TestCase1.dfmea_info["productTree"]["serialNum"], "结构树根节点serialNum错误")

    @allure.title("添加根节点的功能")
    def test_6(self):
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]  # 获取根节点serialNum
        res = functionNodesUpdate().add_function_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, 1)
        pytest.assume(res, "添加功能节点失败")
        TestCase1.added_function1_nodes = res

    @allure.title("添加根节点的失效")
    def test_7(self):
        ppt_serial = TestCase1.added_function1_nodes[0]["pptSerial"]  # 父级产品节点
        pf_serial = TestCase1.added_function1_nodes[0]["serialNum"]  # 父级功能节点
        res = invalidNodesUpdate().add_invalid_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, pf_serial, 1)
        pytest.assume(res, "添加失效节点失败")
        TestCase1.added_invalid1_nodes = res

    @allure.title("结构树添加二级产品节点")
    def test_8(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        product_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        res = productNodesUpdate().add_product_nodes(TestCase1.token, TestCase1.product_type, project_serial,
                                                     product_serial, 1)
        pytest.assume(res, "添加产品节点失败")
        TestCase1.added_product2_nodes = res

    @allure.title("添加二级产品节点的功能")
    def test_9(self):
        ppt_serial = TestCase1.added_product2_nodes[0]["serialNum"]  # 获取第二个产品节点serialNum
        res = functionNodesUpdate().add_function_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, 1)
        pytest.assume(res, "添加功能节点失败")
        TestCase1.added_function2_nodes = res

    @allure.title("添加二级产品节点的失效")
    def test_10(self):
        ppt_serial = TestCase1.added_function2_nodes[0]["pptSerial"]  # 父级产品节点
        pf_serial = TestCase1.added_function2_nodes[0]["serialNum"]  # 父级功能节点
        res = invalidNodesUpdate().add_invalid_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, pf_serial, 1)
        pytest.assume(res, "添加失效节点失败")
        TestCase1.added_invalid2_nodes = res

    @allure.title("添加三级产品节点")
    def test_11(self):
        project_serial = TestCase1.added_product2_nodes[0]["projectSerial"]
        parent_serial = TestCase1.added_product2_nodes[0]["serialNum"]
        res = productNodesUpdate().add_product_nodes(TestCase1.token, TestCase1.product_type, project_serial,
                                                     parent_serial, 1)
        pytest.assume(res, "添加产品节点失败")
        TestCase1.added_product3_nodes = res

    @allure.title("添加三级产品节点的功能")
    def test_12(self):
        ppt_serial = TestCase1.added_product3_nodes[0]["serialNum"]  # 获取第三个产品节点serialNum
        res = functionNodesUpdate().add_function_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, 1)
        pytest.assume(res, "添加功能节点失败")
        TestCase1.added_function3_nodes = res

    @allure.title("添加三级产品节点的失效")
    def test_13(self):
        ppt_serial = TestCase1.added_function3_nodes[0]["pptSerial"]  # 父级产品节点
        pf_serial = TestCase1.added_function3_nodes[0]["serialNum"]  # 父级功能节点
        res = invalidNodesUpdate().add_invalid_nodes(TestCase1.token, TestCase1.product_type, ppt_serial, pf_serial, 1)
        pytest.assume(res, "添加失效节点失败")
        TestCase1.added_invalid3_nodes = res

    @allure.title("功能失效矩阵中添加失效关联")
    def test_14(self):
        first = TestCase1.added_invalid1_nodes[0]  # 获取根节点失效返回信息
        second = TestCase1.added_invalid2_nodes[0]  # 获取二级产品失效返回信息
        res = batchInvalidNetUpdate().batch_invalid_add(TestCase1.token, first, second)
        pytest.assume(res == "1", "添加失效关联失败")

    @allure.title("删除失效关联")
    def test_15(self):
        first_PidSerial = TestCase1.added_invalid1_nodes[0]["serialNum"]  # 获取根节点失效编码
        second_PidSerial = TestCase1.added_invalid2_nodes[0]["serialNum"]  # 获取二级产品失效编码
        res = batchInvalidNetUpdate().batch_invalid_del(TestCase1.token, first_PidSerial, second_PidSerial)
        pytest.assume(res, "删除失效关联失败")

    @allure.title("添加失效原因--下级零件失效")
    def test_16(self):
        pf_serial = TestCase1.added_function2_nodes[0]["serialNum"]
        ppt_serial = TestCase1.added_product2_nodes[0]["serialNum"]
        with allure.step("step1:--查找零件原因"):
            res = selectInvalidReasonList().select_invalid_reason_list_by_product(TestCase1.token,
                                                                                  TestCase1.product_type, pf_serial,
                                                                                  ppt_serial)
            pytest.assume(len(res) > 0, "查找零件原因失败")
        with allure.step("step2:--查找界面原因"):
            res = selectInvalidReasonList().select_reason_list_by_inner_interface(TestCase1.token,
                                                                                  TestCase1.product_type, pf_serial,
                                                                                  ppt_serial)
            pytest.assume(res == [], "查找界面原因失败")
        with allure.step("step3:添加失效原因--下级零件失效"):
            first = TestCase1.added_invalid2_nodes[0]  # 获取二级产品失效返回信息
            second = TestCase1.added_invalid3_nodes[0]  # 获取三级产品失效返回信息
            res = saveInvalidNets().save_invalid_nets(TestCase1.token, first, second)
            pytest.assume(res, "添加零件失效原因失败")
        with allure.step("step4:添加失效原因--保存功能关联"):
            first_pf_serial = first["pfSerial"]
            second_pf_serial = second["pfSerial"]
            second_pfe_serial = second["pfeSerial"]
            res = savePfRelation().save_pf_relation(TestCase1.token, first_pf_serial, second_pf_serial,
                                                    second_pfe_serial)
            pytest.assume(res, "保存功能关联失败")

    @allure.title("添加失效后果--选择上级后果")
    def test_17(self):
        pf_serial = TestCase1.added_function2_nodes[0]["serialNum"]
        ppt_serial = TestCase1.added_product2_nodes[0]["serialNum"]
        with allure.step("step1:--查找上级后果"):
            res = selectInvalidResultList().select_invalid_reason_list_by_product(TestCase1.token,
                                                                                  TestCase1.product_type, pf_serial,
                                                                                  ppt_serial)
            pytest.assume(len(res) > 0, "查找上级后果失败")
        with allure.step("step2:--查找界面原因"):
            res = selectInvalidResultList().select_invalid_result_list_by_inner_interface(TestCase1.token,
                                                                                          TestCase1.product_type,
                                                                                          pf_serial,
                                                                                          ppt_serial)
            pytest.assume(res == [], "查找界面原因失败")
        with allure.step("step3:添加失效后果--上级零件失效"):
            consequence_type = "0271"  # 字典027中name="高一层次影响（对上级影响）"
            first = TestCase1.added_invalid1_nodes[0]  # 获取一级产品失效返回信息
            second = TestCase1.added_invalid2_nodes[0]  # 获取二级产品失效返回信息
            res = saveInvalidNets().save_invalid_nets(TestCase1.token, first, second, 1, consequence_type)
            pytest.assume(res, "添加零件失效后果失败")
        with allure.step("step4:保存功能关联"):
            first_pf_serial = first["pfSerial"]
            first_pfe_serial = first["pfeSerial"]
            second_pf_serial = second["pfSerial"]
            res = savePfRelation().save_consequence_pf_relation(TestCase1.token, first_pf_serial, first_pfe_serial,
                                                                second_pf_serial)
            pytest.assume(res, "保存功能关联失败")

    @allure.title("导出DFMEA报告")
    def test_18(self):
        exportReport().del_last_report()  # 删除上次生成的DFMEA报告
        ppt_serial = TestCase1.added_product2_nodes[0]["serialNum"]  # 获取第二个产品节点serialNum
        with allure.step("step1:导出DFMEA报告--pdf/中文/标准版/单行"):
            exportReport().export_report(TestCase1.token, ppt_serial, "pdf", 1, "0_1_2_3_4_5_6_7", 1, 2,
                                         "dfmea_report1.pdf")
            pytest.assume(os.path.exists("dfmea_report/dfmea_report1.pdf"), "导出失败")
            report1 = os.stat("dfmea_report\dfmea_report1.pdf")
            pytest.assume(report1.st_size > 0, "导出文件大小为0")
        with allure.step("step2:导出DFMEA报告--excel/中文/标准版/单行"):
            exportReport().export_report(TestCase1.token, ppt_serial, "excel", 1, "0_1_2_3_4_5_6_7", 2, 2,
                                         "dfmea_report2.xls")
            pytest.assume(os.path.exists("dfmea_report/dfmea_report2.xls"), "导出失败")
            report2 = os.stat("dfmea_report\dfmea_report2.xls")
            pytest.assume(report2.st_size > 0, "导出文件大小为0")
        with allure.step("step3:导出DFMEA报告--pdf/中英文/新版/合并"):
            exportReport().export_report(TestCase1.token, ppt_serial, "pdf", 1, "0_1_2_3_4_5_6_7", 1, 1,
                                         "dfmea_report3.pdf")
            pytest.assume(os.path.exists("dfmea_report/dfmea_report3.pdf"), "导出失败")
            report3 = os.stat("dfmea_report\dfmea_report3.pdf")
            pytest.assume(report3.st_size > 0, "导出文件大小为0")
        with allure.step("step4:导出DFMEA报告--excel/中英文/新版/合并"):
            exportReport().export_report(TestCase1.token, ppt_serial, "excel", 1, "0_1_2_3_4_5_6_7", 2, 1,
                                         "dfmea_report4.xls")
            pytest.assume(os.path.exists("dfmea_report/dfmea_report4.xls"), "导出失败")
            report4 = os.stat("dfmea_report\dfmea_report4.xls")
            pytest.assume(report4.st_size > 0, "导出文件大小为0")

    @allure.title("删除DFMEA")
    def test_19(self):
        project_serial = TestCase1.dfmea_info["project"]["serialNum"]
        res = deleteDfmea().delete_dfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除DFMEA失败")
