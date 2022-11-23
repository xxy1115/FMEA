# -*- coding: UTF-8 -*-
import os

import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.pfmea_tree import PfmeaTree
from libs.pfmea.add_pfmea import addPFMEA
from libs.pfmea.delete_pfmea import deletePFMEA
from libs.pfmea.element_fun_nodes_update import elementFunNodesUpdate
from libs.pfmea.element_invalid_nodes_update import elementInvalidNodesUpdate
from libs.pfmea.element_nodes_update import elementNodesUpdate
from libs.pfmea.export_pfmea_report import exportPFMEAReport
from libs.pfmea.invalid_parent_result import invalidParentResult
from libs.pfmea.invalid_reason import invalidReason
from libs.pfmea.invalid_result import invalidResult
from libs.pfmea.pfmea_task import PfmeaTask
from libs.pfmea.procedure_fun_nodes_update import procedureFunNodesUpdate
from libs.pfmea.procedure_invalid_nodes_update import procedureInvalidNodesUpdate
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
        self.test_data = parse_yaml("../data/data_05.yaml")

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

    @allure.title("结构树添加三个工序节点")
    def test_6(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        ppp_serial = TestCase1.pfmea_info["projectProcedure"]["serialNum"]
        res = procedureNodesUpdate().add_procedure_nodes(TestCase1.token, TestCase1.product_type, project_serial,
                                                         ppp_serial, 3)
        pytest.assume(res["flag"], "添加工序节点失败")
        TestCase1.added_procedures_nodes = res["pfmeaProjectProcedures"]

    @allure.title("在第一个工序节点添加工序功能")
    def test_7(self):
        serial_num = TestCase1.added_procedures_nodes[0]["serialNum"]
        res = procedureFunNodesUpdate().add_procedure_fun(TestCase1.token, TestCase1.product_type, serial_num, 1)
        pytest.assume(res["flag"], "结构树添加工序功能失败")
        TestCase1.added_procedures_fun_node1 = res["pfmeaProjectFunctions"]

    @allure.title("在第一个工序节点添加失效")
    def test_8(self):
        ppp_serial = TestCase1.added_procedures_fun_node1[0]["projectProcedureSerial"]
        serial_num = TestCase1.added_procedures_fun_node1[0]["serialNum"]
        res = procedureInvalidNodesUpdate().add_procedure_invalid(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                  serial_num, 1)
        pytest.assume(res["flag"], "结构树工序功能添加失效失败")
        TestCase1.added_procedures_invalid_node1 = res["pfmeaProjectInvalids"]

    @allure.title("在第二个工序节点添加工序功能")
    def test_9(self):
        serial_num = TestCase1.added_procedures_nodes[1]["serialNum"]
        res = procedureFunNodesUpdate().add_procedure_fun(TestCase1.token, TestCase1.product_type, serial_num, 1)
        pytest.assume(res["flag"], "结构树添加工序功能失败")
        TestCase1.added_procedures_fun_node2 = res["pfmeaProjectFunctions"]

    @allure.title("在第二个工序节点添加失效")
    def test_10(self):
        ppp_serial = TestCase1.added_procedures_fun_node2[0]["projectProcedureSerial"]
        serial_num = TestCase1.added_procedures_fun_node2[0]["serialNum"]
        res = procedureInvalidNodesUpdate().add_procedure_invalid(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                  serial_num, 1)
        pytest.assume(res["flag"], "结构树工序功能添加失效失败")
        TestCase1.added_procedures_invalid_node2 = res["pfmeaProjectInvalids"]

    @allure.title("在第三个工序节点添加工序功能")
    def test_11(self):
        serial_num = TestCase1.added_procedures_nodes[2]["serialNum"]
        res = procedureFunNodesUpdate().add_procedure_fun(TestCase1.token, TestCase1.product_type, serial_num, 1)
        pytest.assume(res["flag"], "结构树添加工序功能失败")
        TestCase1.added_procedures_fun_node3 = res["pfmeaProjectFunctions"]

    @allure.title("在第三个工序节点添加失效")
    def test_12(self):
        ppp_serial = TestCase1.added_procedures_fun_node3[0]["projectProcedureSerial"]
        serial_num = TestCase1.added_procedures_fun_node3[0]["serialNum"]
        res = procedureInvalidNodesUpdate().add_procedure_invalid(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                  serial_num, 1)
        pytest.assume(res["flag"], "结构树工序功能添加失效失败")
        TestCase1.added_procedures_invalid_node3 = res["pfmeaProjectInvalids"]

    @allure.title("在第二个工序节点添加要素节点")
    def test_13(self):
        ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
        res = elementNodesUpdate().add_element_nodes(TestCase1.token, TestCase1.product_type, ppp_serial, 1)
        pytest.assume(res["flag"], "添加要素节点失败")
        TestCase1.added_element_nodes = res["pfmeaProjectElements"]

    @allure.title("添加要素功能节点")
    def test_14(self):
        pe_serial = TestCase1.added_element_nodes[0]["serialNum"]
        res = elementFunNodesUpdate().add_element_fun_nodes(TestCase1.token, TestCase1.product_type, pe_serial, 1)
        pytest.assume(res["flag"], "添加要素功能节点失败")
        TestCase1.added_ef_nodes = res["pfmeaProjectElementFunctions"]

    @allure.title("添加要素失效节点")
    def test_15(self):
        ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
        ef_serial = TestCase1.added_ef_nodes[0]["serialNum"]
        res = elementInvalidNodesUpdate().add_element_invalid_nodes(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                    ef_serial, 1)
        pytest.assume(res["flag"], "添加要素失效节点失败")
        TestCase1.added_ei_nodes = res["pfmeaProjectInvalids"]

    @allure.title("添加失效原因")
    def test_16(self):
        ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
        with allure.step("step1:下级要素原因列表"):
            res = invalidReason().selectInvalidReasonList(TestCase1.token, ppp_serial)  # 加载下级要素失效列表
            pytest.assume(res, "加载原因列表失败")
            pytest.assume(len(res["invalidReasonList"]) > 0, "原因列表数据空")
        with allure.step("step2:添加下级要素失效作为失效原因-saveFeatureMatrixRelation"):
            ef_serial = TestCase1.added_ef_nodes[0]["serialNum"]
            pf_serial = TestCase1.added_procedures_fun_node2[0]["serialNum"]  # 第二个工序功能节点
            res = invalidReason().saveFeatureMatrixRelation(TestCase1.token, ef_serial, pf_serial)
            pytest.assume(res["flag"] == "1", "saveFeatureMatrixRelation接口失败")
        with allure.step("step3:添加下级要素失效作为失效原因-saveOrUpdate"):
            res = invalidReason().saveOrUpdate(TestCase1.token)
            pytest.assume(res["flag"], "saveOrUpdate接口失败")
        with allure.step("step4:添加下级要素失效作为失效原因-saveInvalidNets"):
            firstPfSerial = pf_serial
            firstPidSerial = TestCase1.added_procedures_invalid_node2[0]["serialNum"]
            firstPpSerial = TestCase1.added_procedures_fun_node2[0]["serialNum"]
            secondPeSerial = TestCase1.added_element_nodes[0]["serialNum"]
            secondPfSerial = TestCase1.added_ef_nodes[0]["serialNum"]
            secondPidSerial = TestCase1.added_ei_nodes[0]["serialNum"]
            res = invalidReason().saveInvalidNets(TestCase1.token, firstPfSerial, firstPidSerial, firstPpSerial,
                                                  secondPeSerial, secondPfSerial,
                                                  secondPidSerial)
            pytest.assume(res["flag"], "saveInvalidNets接口失败")

    @allure.title("添加上工序原因")
    def test_17(self):
        ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
        with allure.step("step1:上工序原因列表"):
            res = invalidReason().findPreProcedureFailure(TestCase1.token, TestCase1.product_type, ppp_serial)
            pytest.assume(res["flag"], "加载上工序原因列表失败")
            pytest.assume(len(res["items"]) > 0, "上工序原因列表数据空")
        with allure.step("step2:添加上工序失效作为失效原因"):
            preProcedureFailureSerial = TestCase1.added_procedures_invalid_node1[0]["serialNum"]
            preProcedureSerial = TestCase1.added_procedures_nodes[0]["serialNum"]
            procedureFailureSerial = TestCase1.added_procedures_invalid_node2[0]["serialNum"]
            procedureSerial = TestCase1.added_procedures_nodes[1]["serialNum"]
            res = invalidReason().saveFailureRelation(TestCase1.token, preProcedureFailureSerial, preProcedureSerial,
                                                      procedureFailureSerial, procedureSerial)
            pytest.assume(res["flag"], "添加上工序失效原因失败")

    @allure.title("添加后工序后果")
    def test_18(self):
        with allure.step("step1:后工序后果列表"):
            ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
            res = invalidResult().findNextProcedureFailure(TestCase1.token, TestCase1.product_type, ppp_serial)
            pytest.assume(res["flag"], "后工序后果列表加载失败")
            pytest.assume(len(res["items"]) > 0, "后工序后果列表数据空")
        with allure.step("step2:添加后工序后果保存"):
            preProcedureFailureSerial = TestCase1.added_procedures_invalid_node2[0]["serialNum"]
            preProcedureSerial = TestCase1.added_procedures_nodes[1]["serialNum"]
            procedureFailureSerial = TestCase1.added_procedures_invalid_node3[0]["serialNum"]
            procedureSerial = TestCase1.added_procedures_nodes[2]["serialNum"]
            res = invalidResult().saveFailureRelation(TestCase1.token, preProcedureFailureSerial, preProcedureSerial,
                                                      procedureFailureSerial, procedureSerial)
            pytest.assume(res["flag"], "添加后工序后果失败")

    @allure.title("在根节点添加功能")
    def test_19(self):
        serial_num = TestCase1.pfmea_info["projectProcedure"]["serialNum"]
        res = procedureFunNodesUpdate().add_procedure_fun(TestCase1.token, TestCase1.product_type, serial_num, 1)
        pytest.assume(res["flag"], "根节点添加功能失败")
        TestCase1.root_fun_node = res["pfmeaProjectFunctions"]

    @allure.title("在根节点添加失效")
    def test_20(self):
        ppp_serial = TestCase1.root_fun_node[0]["projectProcedureSerial"]
        serial_num = TestCase1.root_fun_node[0]["serialNum"]
        res = procedureInvalidNodesUpdate().add_procedure_invalid(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                  serial_num, 1)
        pytest.assume(res["flag"], "结构树工序功能添加失效失败")
        TestCase1.root_invalid_node = res["pfmeaProjectInvalids"]

    @allure.title("添加后果-上级失效")
    def test_21(self):
        with allure.step("step1:上级失效列表"):
            ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]
            res = invalidParentResult().findParentProcedureFailure(TestCase1.token, TestCase1.product_type, ppp_serial)
            pytest.assume(res["flag"], "上级失效列表接口失败")
            pytest.assume(len(res["items"]) > 0, "上级失效列表数据空")
        with allure.step("step2:添加上级失效作为失效后果-saveFeatureMatrixRelation"):
            pf_serial = TestCase1.added_procedures_fun_node2[0]["serialNum"]
            parent_pf_serial = TestCase1.root_fun_node[0]["serialNum"]
            res = invalidParentResult().saveFeatureMatrixRelation(TestCase1.token, pf_serial, parent_pf_serial)
            pytest.assume(res["flag"] == "1", "saveFeatureMatrixRelation接口失败")
        with allure.step("step3:添加上级失效作为失效后果-saveOrUpdate"):
            res = invalidParentResult().saveOrUpdate(TestCase1.token)
            pytest.assume(res["flag"], "saveOrUpdate接口失败")
        with allure.step("step4:添加上级失效作为失效后果-saveInvalidNets"):
            feature = TestCase1.root_fun_node[0]["procedureFunctionName"]
            en_feature = TestCase1.root_fun_node[0]["enFunction"]
            firstPfSerial = TestCase1.root_fun_node[0]["serialNum"]
            firstPidSerial = TestCase1.root_invalid_node[0]["serialNum"]
            secondPfSerial = TestCase1.added_procedures_fun_node2[0]["serialNum"]
            secondPidSerial = TestCase1.added_procedures_invalid_node2[0]["serialNum"]
            secondPpSerial = TestCase1.added_procedures_nodes[1]["serialNum"]
            res = invalidParentResult().saveInvalidNets(TestCase1.token, feature, en_feature, firstPfSerial,
                                                        firstPidSerial, secondPfSerial, secondPidSerial, secondPpSerial)
            pytest.assume(res["flag"], "saveInvalidNets接口失败")

    @allure.title("导出PFMEA报告")
    def test_22(self):
        exportPFMEAReport().del_last_report()  # 删除上次生成的DFMEA报告
        ppp_serial = TestCase1.added_procedures_nodes[1]["serialNum"]  # 获取第二个工序节点serialNum
        with allure.step("step1:导出PFMEA报告--pdf/中文/标准版/单行"):
            exportPFMEAReport().export_pfmea_report(TestCase1.token, ppp_serial, "pdf", "1", "0_1_2_3_4_5_6_7_a", "1",
                                                    "2", "pfmea_report1.pdf")
            pytest.assume(os.path.exists("pfmea_report/pfmea_report1.pdf"), "导出失败")
            report1 = os.stat("pfmea_report\pfmea_report1.pdf")
            pytest.assume(report1.st_size > 0, "导出文件大小为0")
        with allure.step("step2:导出PFMEA报告--excel/中文/标准版/单行"):
            exportPFMEAReport().export_pfmea_report(TestCase1.token, ppp_serial, "excel", "1", "0_1_2_3_4_5_6_7_a", "1",
                                                    "2", "pfmea_report2.xls")
            pytest.assume(os.path.exists("pfmea_report/pfmea_report2.xls"), "导出失败")
            report2 = os.stat("pfmea_report\pfmea_report2.xls")
            pytest.assume(report2.st_size > 0, "导出文件大小为0")
        with allure.step("step3:导出PFMEA报告--pdf/中英文/新版/合并"):
            exportPFMEAReport().export_pfmea_report(TestCase1.token, ppp_serial, "pdf", "1", "0_1_2_3_4_5_6_7_a", "2",
                                                    "1", "pfmea_report3.pdf")
            pytest.assume(os.path.exists("pfmea_report/pfmea_report3.pdf"), "导出失败")
            report3 = os.stat("pfmea_report\pfmea_report3.pdf")
            pytest.assume(report3.st_size > 0, "导出文件大小为0")
        with allure.step("step4:导出PFMEA报告--excel/中英文/新版/合并"):
            exportPFMEAReport().export_pfmea_report(TestCase1.token, ppp_serial, "excel", "1", "0_1_2_3_4_5_6_7_a", "2",
                                                    "1", "pfmea_report4.xls")
            pytest.assume(os.path.exists("pfmea_report/pfmea_report4.xls"), "导出失败")
            report4 = os.stat("pfmea_report\pfmea_report4.xls")
            pytest.assume(report4.st_size > 0, "导出文件大小为0")

    @allure.title("删除PFMEA")
    def test_23(self):
        project_serial = TestCase1.pfmea_info["projectProcedure"]["projectSerial"]
        res = deletePFMEA().delete_pfmea(TestCase1.token, project_serial)
        pytest.assume(res["flag"], "删除PFMEA失败")
