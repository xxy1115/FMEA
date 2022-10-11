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
from libs.pfmea.element_fea_nodes_update import elementFeaNodesUpdate
from libs.pfmea.element_fun_nodes_update import elementFunNodesUpdate
from libs.pfmea.element_invalid_nodes_update import elementInvalidNodesUpdate
from libs.pfmea.element_nodes_update import elementNodesUpdate
from libs.pfmea.measure_p_nodes_update import measurePNodesUpdate
from libs.pfmea.pfmea_task import PfmeaTask
from libs.pfmea.procedure_nodes_update import procedureNodesUpdate
from libs.program_list import programList
from utils.yamlControl import parse_yaml


class TestCase1:
    token = "e38c5f55dd1d4807a0ef763a13e186f8"
    user_id = 1681
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
    def atest_1(self):
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

    @allure.title("结构树编辑工序节点")
    def test_7(self):
        serial_num = TestCase1.added_procedures_nodes[0]["serialNum"]  # 编辑第一个工序节点
        res = procedureNodesUpdate().edit_procedure_nodes(TestCase1.token, TestCase1.product_type, serial_num)
        pytest.assume(res["flag"], "编辑工序节点失败")
        res["pfmeaProjectProcedure"]

    @allure.title("结构树删除工序节点")
    def test_8(self):
        serial_num = TestCase1.added_procedures_nodes[1]["serialNum"]  # 删除第二个工序节点
        res = procedureNodesUpdate().del_procedure_nodes(TestCase1.token, serial_num)
        pytest.assume(res["flag"], "删除工序节点失败")

    @allure.title("结构树添加要素节点")
    def test_9(self):
        ppp_serial = TestCase1.added_procedures_nodes[2]["serialNum"]  # 在第三个工序节点添加要素
        res = elementNodesUpdate().add_element_nodes(TestCase1.token, TestCase1.product_type, ppp_serial, 3)
        pytest.assume(res["flag"], "添加要素节点失败")
        TestCase1.added_element_nodes = res["pfmeaProjectElements"]

    @allure.title("结构树编辑要素节点")
    def test_10(self):
        serial_num = TestCase1.added_element_nodes[0]["serialNum"]  # 编辑第一个要素节点
        res = elementNodesUpdate().edit_element_nodes(TestCase1.token, TestCase1.product_type, serial_num)
        pytest.assume(res["flag"], "编辑要素节点失败")

    @allure.title("结构树删除要素节点")
    def test_11(self):
        serial_num = TestCase1.added_element_nodes[1]["serialNum"]  # 删除第二个要素节点
        projectProcedureSerial = TestCase1.added_element_nodes[1]["projectProcedureSerial"]  # 删除第二个要素节点
        res = elementNodesUpdate().del_element_nodes(TestCase1.token, serial_num, projectProcedureSerial)
        pytest.assume(res["flag"], "删除要素节点失败")

    @allure.title("结构树添加要素功能节点")
    def test_12(self):
        pe_serial = TestCase1.added_element_nodes[2]["serialNum"]  # 在第三个要素节点添加要素功能
        res = elementFunNodesUpdate().add_element_fun_nodes(TestCase1.token, TestCase1.product_type, pe_serial, 3)
        pytest.assume(res["flag"], "添加要素功能节点失败")
        TestCase1.added_ef_nodes = res["pfmeaProjectElementFunctions"]

    @allure.title("结构树编辑要素功能节点")
    def test_13(self):
        serial_num = TestCase1.added_ef_nodes[0]["serialNum"]  # 编辑第一个要素功能节点
        res = elementFunNodesUpdate().edit_element_fun_nodes(TestCase1.token, TestCase1.product_type, serial_num)
        pytest.assume(res["flag"], "编辑要素节点失败")

    @allure.title("结构树删除要素功能节点")
    def test_14(self):
        serial_num = TestCase1.added_ef_nodes[1]["serialNum"]  # 删除第二个要素功能节点
        res = elementFunNodesUpdate().del_element_fun_nodes(TestCase1.token, serial_num)
        pytest.assume(res["flag"], "删除要素功能节点失败")

    @allure.title("结构树添加要素失效节点")
    def test_15(self):
        ppp_serial = TestCase1.added_procedures_nodes[2]["serialNum"]
        ef_serial = TestCase1.added_ef_nodes[2]["serialNum"]  # 在第三个要素功能节点添加要素失效
        res = elementInvalidNodesUpdate().add_element_invalid_nodes(TestCase1.token, TestCase1.product_type, ppp_serial,
                                                                    ef_serial, 3)
        pytest.assume(res["flag"], "添加要素失效节点失败")
        TestCase1.added_ei_nodes = res["pfmeaProjectInvalids"]

    @allure.title("结构树编辑要素失效节点")
    def test_16(self):
        serial_num = TestCase1.added_ei_nodes[0]["serialNum"]  # 编辑第一个要素失效节点
        res = elementInvalidNodesUpdate().edit_element_invalid_nodes(TestCase1.token, TestCase1.product_type,
                                                                     serial_num)
        pytest.assume(res["flag"], "编辑要素失效节点失败")

    @allure.title("结构树删除要素失效节点")
    def test_17(self):
        ppp_serial = TestCase1.added_procedures_nodes[2]["serialNum"]
        serial_num = TestCase1.added_ei_nodes[1]["serialNum"]  # 删除第二个要素失效节点
        res = elementInvalidNodesUpdate().del_element_invalid_nodes(TestCase1.token, ppp_serial, serial_num)
        pytest.assume(res["flag"], "删除要素失效节点失败")

    @allure.title("结构树添加预防措施节点")
    def test_18(self):
        ei_serial = TestCase1.added_ei_nodes[2]["serialNum"]  # 在第三个要素失效节点添加预防措施
        res = measurePNodesUpdate().add_measure_occ(TestCase1.token, TestCase1.product_type, ei_serial, 3)
        pytest.assume(res["flag"], "添加预防措施节点失败")
        TestCase1.added_measure_o_nodes = res["projectMeasures"]

    @allure.title("结构树编辑预防措施节点")
    def test_19(self):
        serial_num = TestCase1.added_measure_o_nodes[0]["serialNum"]  # 编辑第一个预防措施节点
        pidSerial = TestCase1.added_measure_o_nodes[0]["pidSerial"]
        projectSerial = TestCase1.pfmea_info["pfmeaProject"]["serialNum"]
        res = measurePNodesUpdate().edit_measure_occ(TestCase1.token, TestCase1.product_type, serial_num, pidSerial,
                                                     projectSerial)
        pytest.assume(res["flag"], "编辑预防措施节点失败")

    @allure.title("结构树删除预防措施节点")
    def test_20(self):
        ppp_serial = TestCase1.added_procedures_nodes[2]["serialNum"]
        serial_num = TestCase1.added_measure_o_nodes[1]["serialNum"]  # 删除第二个预防措施节点
        invalidMode = TestCase1.added_ei_nodes[2]["invalidmodeName"]
        res = measurePNodesUpdate().del_measure_occ(TestCase1.token, invalidMode, ppp_serial, serial_num)
        pytest.assume(res["flag"], "删除预防措施节点失败")

    @allure.title("结构树添加探测措施节点")
    def test_21(self):
        ei_serial = TestCase1.added_ei_nodes[2]["serialNum"]  # 在第三个要素失效节点添加预防措施
        res = measurePNodesUpdate().add_measure_det(TestCase1.token, TestCase1.product_type, ei_serial, 3)
        pytest.assume(res["flag"], "添加探测措施节点失败")
        TestCase1.added_measure_d_nodes = res["projectMeasures"]

    @allure.title("结构树编辑探测措施节点")
    def test_22(self):
        serial_num = TestCase1.added_measure_d_nodes[0]["serialNum"]  # 编辑第一个探测措施节点
        pidSerial = TestCase1.added_measure_d_nodes[0]["pidSerial"]
        projectSerial = TestCase1.pfmea_info["pfmeaProject"]["serialNum"]
        res = measurePNodesUpdate().edit_measure_det(TestCase1.token, TestCase1.product_type, serial_num, pidSerial,
                                                     projectSerial)
        pytest.assume(res["flag"], "编辑探测措施节点失败")

    @allure.title("结构树删除探测措施节点")
    def test_23(self):
        ppp_serial = TestCase1.added_procedures_nodes[2]["serialNum"]
        serial_num = TestCase1.added_measure_d_nodes[1]["serialNum"]  # 删除第二个探测措施节点
        invalidMode = TestCase1.added_ei_nodes[2]["invalidmodeName"]
        res = measurePNodesUpdate().del_measure_det(TestCase1.token, invalidMode, ppp_serial, serial_num)
        pytest.assume(res["flag"], "删除探测措施节点失败")

    @allure.title("结构树添加过程特性节点")
    def test_24(self):
        pe_serial = TestCase1.added_element_nodes[2]["serialNum"]  # 在第三个要素节点添加过程特性
        res = elementFeaNodesUpdate().add_element_fea_nodes(TestCase1.token, TestCase1.product_type, pe_serial, 3)
        pytest.assume(res["flag"], "添加过程特性节点失败")
        TestCase1.added_pc_nodes = res["pfmeaProjectFeatures"]

    @allure.title("结构树编辑过程特性节点")
    def test_25(self):
        serial_num = TestCase1.added_pc_nodes[0]["serialNum"]  # 编辑第一个过程特性节点
        res = elementFeaNodesUpdate().edit_element_fea_nodes(TestCase1.token, TestCase1.product_type, serial_num)
        pytest.assume(res["flag"], "编辑过程特性失败")

    @allure.title("结构树删除过程特性节点")
    def test_26(self):
        serial_num = TestCase1.added_pc_nodes[1]["serialNum"]  # 删除第二个过程特性节点
        res = elementFeaNodesUpdate().del_element_fea_nodes(TestCase1.token, serial_num)
        pytest.assume(res["flag"], "删除过程特性节点失败")
