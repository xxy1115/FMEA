# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_product import getProduct
from common.login import Login
from libs.dfmea.feature_nodes_update import featureNodesUpdate
from libs.dfmea.function_nodes_update import functionNodesUpdate
from libs.dfmea.invalid_nodes_update import invalidNodesUpdate
from libs.dfmea.measure_nodes_update import measureNodesUpdate
from libs.dfmea.product_nodes_update import productNodesUpdate
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.dfmea_tree import DfmeaTree
from libs.dfmea.reason_nodes_update import reasonNodesUpdate
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
    added_product_nodes = []  # 添加的产品节点
    added_function_nodes = []  # 添加的功能节点
    added_feature_nodes = []  # 添加的特性节点
    added_invalid_nodes = []  # 添加的失效节点
    added_reason_nodes = []  # 添加的失效原因节点
    save_invalid_nets = []  # 保存失效网
    added_measure_p_nodes = []  # 添加的预防措施节点
    added_measure_d_nodes = []  # 添加的探测措施节点

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
            # print(json.dumps(res.json()["data"], indent=2))

    @allure.title("获取DFMEA结构树")
    def test_5(self):
        serial_num = TestCase1.dfmea_info["project"]["serialNum"]
        res = DfmeaTree().dfmea_tree(TestCase1.token, serial_num)
        pytest.assume(res, "获取DFMEA结构树失败")
        pytest.assume(res["data"]["text"] == TestCase1.dfmea_info["project"]["productName"], "结构树根节点产品名称错误")
        pytest.assume(res["data"]["pptSerial"] == TestCase1.dfmea_info["productTree"]["serialNum"], "结构树根节点serialNum错误")

    @allure.title("结构树添加产品节点")
    def test_6(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        product_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        res = productNodesUpdate().add_product_nodes(self.test_data["add_product_nodes"], TestCase1.token,
                                                     TestCase1.product_type,
                                                     project_serial, product_serial)
        pytest.assume(res, "添加产品节点失败")
        TestCase1.added_product_nodes = res

    @allure.title("结构树编辑产品节点")
    def test_7(self):
        serial_num = TestCase1.added_product_nodes[0]["serialNum"]  # 编辑第一个产品节点
        res = productNodesUpdate().edit_product_nodes(self.test_data["edit_product_nodes"], TestCase1.token,
                                                      TestCase1.product_type,
                                                      serial_num)
        pytest.assume(res == 1, "编辑产品节点失败")

    @allure.title("结构树删除产品节点")
    def test_8(self):
        serial_num = TestCase1.added_product_nodes[1]["serialNum"]  # 删除第二个产品节点
        res = productNodesUpdate().del_product_nodes(TestCase1.token, serial_num)
        pytest.assume(res["flag"] == "1", "删除产品节点失败")

    @allure.title("结构树添加功能节点")
    def test_9(self):
        ppt_serial = TestCase1.added_product_nodes[2]["serialNum"]  # 在第三个产品节点添加功能
        res = functionNodesUpdate().add_function_nodes(self.test_data["add_function_nodes"], TestCase1.token,
                                                       TestCase1.product_type, ppt_serial)
        pytest.assume(res, "添加功能节点失败")
        TestCase1.added_function_nodes = res

    @allure.title("结构树编辑功能节点")
    def test_10(self):
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        serial_num = TestCase1.added_function_nodes[0]["serialNum"]  # 编辑第一个功能节点
        res = functionNodesUpdate().edit_function_nodes(self.test_data["edit_function_nodes"], TestCase1.token,
                                                        TestCase1.product_type, project_serial, serial_num)
        pytest.assume(res == 1, "编辑功能节点失败")

    @allure.title("结构树删除功能节点")
    def test_11(self):
        serial_num = TestCase1.added_function_nodes[1]["serialNum"]  # 删除第二个功能节点
        fun_name = TestCase1.added_function_nodes[1]["functionName1"]
        pif_serial = TestCase1.added_function_nodes[1]["pifSerial"]
        res = functionNodesUpdate().del_function_nodes(TestCase1.token, serial_num, fun_name, pif_serial)
        pytest.assume(res, "删除功能节点失败")

    @allure.title("结构树添加特性节点")
    def test_12(self):
        ppt_serial = TestCase1.added_product_nodes[2]["serialNum"]  # 在第三个产品节点添加特性
        res = featureNodesUpdate().add_feature_nodes(self.test_data["add_feature_nodes"], TestCase1.token,
                                                     TestCase1.product_type, ppt_serial)
        pytest.assume(res, "添加特性节点失败")
        TestCase1.added_feature_nodes = res

    @allure.title("结构树编辑特性节点")
    def test_13(self):
        serial_num = TestCase1.added_feature_nodes[0]["serialNum"]  # 编辑第一个特性节点
        res = featureNodesUpdate().edit_feature_nodes(self.test_data["edit_feature_nodes"], TestCase1.token,
                                                        TestCase1.product_type, serial_num)
        pytest.assume(res, "编辑特性节点失败")

    @allure.title("结构树删除特性节点")
    def test_14(self):
        serial_num = TestCase1.added_feature_nodes[1]["serialNum"]  # 删除第二个特性节点
        res = featureNodesUpdate().del_feature_nodes(TestCase1.token, serial_num)
        pytest.assume(res, "删除特性节点失败")

    @allure.title("结构树添加失效节点")
    def test_15(self):
        # 在第三个功能节点添加失效
        ppt_serial = TestCase1.added_function_nodes[2]["pptSerial"]  # 父级产品节点
        pf_serial = TestCase1.added_function_nodes[2]["serialNum"]  # 父级功能节点
        res = invalidNodesUpdate().add_invalid_nodes(self.test_data["add_invalid_nodes"], TestCase1.token,
                                                     TestCase1.product_type, ppt_serial, pf_serial)
        pytest.assume(res, "添加失效节点失败")
        TestCase1.added_invalid_nodes = res

    @allure.title("结构树编辑失效节点")
    def test_16(self):
        # 编辑第一个失效节点
        serial_num = TestCase1.added_invalid_nodes[0]["serialNum"]  # 获取节点serialNum
        res = invalidNodesUpdate().edit_invalid_nodes(self.test_data["edit_invalid_nodes"], TestCase1.token,
                                                      TestCase1.product_type, serial_num)
        pytest.assume(res == 1, "编辑失效节点失败")

    @allure.title("结构树删除失效节点")
    def test_17(self):
        # 删除第二个失效节点
        serial_num = TestCase1.added_invalid_nodes[1]["serialNum"]  # 获取节点serialNum
        pif_serial = TestCase1.added_invalid_nodes[1]["pifSerial"]  # 获取节点pifSerial
        invalid_name = TestCase1.added_invalid_nodes[1]["invalidmodeName"]
        res = invalidNodesUpdate().del_invalid_nodes(TestCase1.token, invalid_name, pif_serial, serial_num)
        pytest.assume(res, "接口响应失败")
        pytest.assume(res["flag"], "删除失效节点失败")

    @allure.title("结构树添加失效原因节点")
    def test_18(self):
        # 在第三个失效节点添加失效原因
        node_data = TestCase1.added_invalid_nodes[2]  # 获取第三个失效节点
        project_invalids, project_invalid_nets, save_pf_relation = reasonNodesUpdate().add_reason_nodes(
            self.test_data["add_reason_nodes"], TestCase1.token,
            TestCase1.product_type, node_data)
        pytest.assume(project_invalids, "添加失效原因失败")
        pytest.assume(project_invalid_nets, "保存失效网失败")
        pytest.assume(save_pf_relation, "保存功能网失败")
        TestCase1.added_reason_nodes = project_invalids
        TestCase1.save_invalid_nets = project_invalid_nets

    @allure.title("结构树编辑失效原因节点")
    def test_19(self):
        # 编辑第一个失效原因节点
        serial_num = TestCase1.save_invalid_nets[0]["serialNum"]  # 获取节点serialNum
        res = reasonNodesUpdate().edit_reason_nodes(self.test_data["edit_reason_nodes"], TestCase1.token,
                                                    TestCase1.product_type, serial_num)
        pytest.assume(res, "编辑失效原因失败")
        TestCase1.update_invalid_nets = res

    @allure.title("结构树删除失效原因节点")
    def test_20(self):
        # 删除第二个失效原因节点
        name = TestCase1.save_invalid_nets[1]["secondPidName"]  # 获取失效原因名称(second表示存在一个上级失效)
        serial_num = TestCase1.save_invalid_nets[1]["serialNum"]  # 获取失效原因serialNum
        pif_serial = TestCase1.save_invalid_nets[1]["pifSerial"]  # 获取失效原因界面功能
        res = reasonNodesUpdate().del_reason_nodes(TestCase1.token, name, pif_serial, serial_num)
        pytest.assume(res, "删除失效原因失败")

    @allure.title("结构树添加预防措施节点")
    def test_21(self):
        # 在第三个失效原因节点添加预防措施
        pid_serial = TestCase1.save_invalid_nets[2]["serialNum"]  # 获取失效原因serialNum
        pif_serial = TestCase1.save_invalid_nets[2]["pifSerial"]  # 获取失效原因界面功能
        flag, change_reason_list, project_measures = measureNodesUpdate().add_measure_nodes(
            self.test_data["add_p_nodes"], TestCase1.token,
            TestCase1.product_type, pid_serial, pif_serial)
        pytest.assume(flag, "添加预防措施失败")
        TestCase1.change_reason_list = change_reason_list
        TestCase1.added_measure_p_nodes = project_measures

    @allure.title("结构树编辑预防措施节点")
    def test_22(self):
        # 编辑第一个预防措施
        project_serial = TestCase1.added_product_nodes[2]["projectSerial"]  # 获取dfmea项目节点
        ppt_serial = TestCase1.added_product_nodes[2]["serialNum"]  # 获取上级产品节点
        serial_num = TestCase1.added_measure_p_nodes[0]["serialNum"]
        pid_serial = TestCase1.added_measure_p_nodes[0]["pidSerial"]
        res = measureNodesUpdate().edit_measure_nodes(self.test_data["edit_p_nodes"], TestCase1.token,
                                                      TestCase1.product_type, pid_serial,
                                                      serial_num, project_serial, ppt_serial)
        pytest.assume(res, "接口响应失败")
        pytest.assume(res["flag"] == 1, "编辑预防措施失败")

    @allure.title("结构树删除预防措施节点")
    def test_23(self):
        # 删除第二个预防措施
        measure_name = TestCase1.added_measure_p_nodes[1]["measuresName"]
        pid_serial = TestCase1.added_measure_p_nodes[1]["pidSerial"]
        serial_num = TestCase1.added_measure_p_nodes[1]["serialNum"]
        reason_name = TestCase1.change_reason_list[0]["reasonName"]
        ppt_serial = TestCase1.change_reason_list[0]["firstPptSerial"]
        res = measureNodesUpdate().del_measure_nodes(TestCase1.token, measure_name, pid_serial, serial_num, reason_name,
                                                     ppt_serial)
        pytest.assume(res, "接口响应失败")
        pytest.assume(res["flag"], "删除预防措施失败")

    @allure.title("结构树添加探测措施节点")
    def test_24(self):
        # 在第三个失效原因节点添加探测措施
        pid_serial = TestCase1.save_invalid_nets[2]["serialNum"]  # 获取失效原因serialNum
        pif_serial = TestCase1.save_invalid_nets[2]["pifSerial"]  # 获取失效原因界面功能
        flag, change_reason_list, project_measures = measureNodesUpdate().add_measure_nodes(
            self.test_data["add_d_nodes"], TestCase1.token,
            TestCase1.product_type, pid_serial, pif_serial)
        pytest.assume(flag, "添加预防措施失败")
        TestCase1.change_reason_list = change_reason_list
        TestCase1.added_measure_d_nodes = project_measures

    @allure.title("结构树编辑探测措施节点")
    def test_25(self):
        # 编辑第一个探测措施
        project_serial = TestCase1.added_product_nodes[2]["projectSerial"]  # 获取dfmea项目节点
        ppt_serial = TestCase1.added_product_nodes[2]["serialNum"]  # 获取上级产品节点
        serial_num = TestCase1.added_measure_d_nodes[0]["serialNum"]
        pid_serial = TestCase1.added_measure_d_nodes[0]["pidSerial"]
        res = measureNodesUpdate().edit_measure_nodes(self.test_data["edit_d_nodes"], TestCase1.token,
                                                      TestCase1.product_type, pid_serial,
                                                      serial_num, project_serial, ppt_serial)
        pytest.assume(res, "接口响应失败")
        pytest.assume(res["flag"] == 1, "编辑探测措施失败")

    @allure.title("结构树删除探测措施节点")
    def test_26(self):
        # 删除第二个探测措施
        measure_name = TestCase1.added_measure_d_nodes[1]["measuresName"]
        pid_serial = TestCase1.added_measure_d_nodes[1]["pidSerial"]
        serial_num = TestCase1.added_measure_d_nodes[1]["serialNum"]
        reason_name = TestCase1.change_reason_list[0]["reasonName"]
        ppt_serial = TestCase1.change_reason_list[0]["firstPptSerial"]
        res = measureNodesUpdate().del_measure_nodes(TestCase1.token, measure_name, pid_serial, serial_num, reason_name,
                                                     ppt_serial)
        pytest.assume(res, "接口响应失败")
        pytest.assume(res["flag"], "删除探测措施失败")
