# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_function_group import getFunctionGroup
from common.get_invalid_model import getInvalidModel
from common.get_product import getProduct
from common.login import Login
from common.select_feature_product_type_by_serial import selectFeatureProductTypeBySerialNum
from common.select_function_product_type_by_serial import selectFunctionProductTypeBySerialNum
from common.select_invalid_product_type_by_serial import selectInvalidProductTypeBySerialNum
from common.select_product_by_pptSerial import selectProductByPptSerial
from libs.dfmea.dfmea_task import DfmeaTask
from libs.dfmea.add_dfmea import addDFMEA
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.dfmea.dfmea_tree import DfmeaTree
from libs.dfmea.save_feature import saveFeature
from libs.dfmea.save_function import saveFunction
from libs.dfmea.save_invalid import saveInvalid
from libs.dfmea.save_measure import saveMeasure
from libs.dfmea.save_reason import saveReason
from libs.program_list import programList
from libs.save_product import saveProduct
from utils.yamlControl import parse_yaml


class TestCase1:
    token = ""
    user_id = 1681
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    dfmea_info = {}  # 创建DFMEA返回信息
    project_task_num = ""  # DFMEA任务编号
    product_types = []  # 产品类别
    added_product_nodes = []  # 产品节点信息
    added_function_nodes = []  # 功能节点信息
    added_feature_nodes = []  # 特性节点信息
    applicableObject = "13e553bc150b4ca58e174ce67dd158cb"  # 适用对象(D)

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
            flag, task_num = DfmeaTask().dfmea_task(TestCase1.token, TestCase1.user_id, project, role_type)
            pytest.assume(flag, "创建DFMEA任务失败")
            TestCase1.project_task_num = task_num  # 获取任务编号DFMEA新建任务使用
            print(task_num)

    @allure.title("获取DFMEA结构树")
    def test_5(self):
        serial_num = TestCase1.dfmea_info["project"]["serialNum"]
        res = DfmeaTree().dfmea_tree(TestCase1.token, serial_num)
        pytest.assume(res, "获取DFMEA结构树失败")
        pytest.assume(res["data"]["text"] == TestCase1.dfmea_info["project"]["productName"], "结构树根节点产品名称错误")
        pytest.assume(res["data"]["pptSerial"] == TestCase1.dfmea_info["productTree"]["serialNum"], "结构树根节点serialNum错误")

    @allure.title("结构树添加产品节点--创建产品")
    def test_6(self):
        # ppt_serial = "bb24bf56fdcf4b3d8f7185cde688dfb7"
        # project_serial = "34d785ef6d5d4b5f871ec62bf625e41a"
        project_serial = TestCase1.dfmea_info["productTree"]["projectSerial"]
        ppt_serial = TestCase1.dfmea_info["productTree"]["serialNum"]
        product_level = TestCase1.dicts["004"][0]["code"]  # 层级
        with allure.step("step1:获取上级产品类别"):
            res = selectProductByPptSerial().select_product_by_pptSerial(TestCase1.token, ppt_serial)  # 获取productTypes
            pytest.assume(res, "获取产品类别失败")
            TestCase1.product_types = res["productTypes"]
        with allure.step("step2:结构树创建产品"):
            flag, max_num = saveProduct().save_product(TestCase1.token, product_level,
                                                       TestCase1.product_types)
            pytest.assume(flag, "新建产品失败")
        with allure.step("step3:添加刚创建的产品"):
            res = saveProduct().add_product(TestCase1.token, TestCase1.product_type, ppt_serial, project_serial,
                                            max_num)
            pytest.assume(res, " ")
            TestCase1.added_product_nodes = res

    @allure.title("结构树添加功能节点--创建功能")
    def test_7(self):
        types = [TestCase1.dicts["008"][0]["code"]]  # 功能分类 functionTypes
        category = TestCase1.dicts["016"][0]["code"]  # 功能类别 functionCategory
        with allure.step("step1:结构树创建功能"):
            result, en_function, function = saveFunction().save_function(TestCase1.token, types, category,
                                                                         TestCase1.product_types)  # 传上级的产品类别
            pytest.assume(result["flag"], "创建功能失败")
            serial_num = result["serialNum"]
        with allure.step("step2:添加刚创建的功能"):
            ppt_serial = TestCase1.added_product_nodes[0]["serialNum"]
            res = saveFunction().add_function(TestCase1.token, en_function, function, serial_num, ppt_serial)
            pytest.assume(res, "添加功能节点失败")
            TestCase1.added_function_nodes = res

    @allure.title("结构树添加特性节点--创建特性")
    def test_8(self):
        pf_serial = TestCase1.added_function_nodes[0]["serialNum"]
        with allure.step("step1:获取上级产品类别"):
            res = selectFunctionProductTypeBySerialNum().select_f_p_t_by_serial(TestCase1.token, pf_serial)
            pytest.assume(res, "获取产品类别失败")
            product_types = res["productTypes"]
        with allure.step("step2:结构树创建特性"):
            product_feature_category = saveFeature().save_feature(TestCase1.token, product_types)
            pytest.assume(product_feature_category, "创建特性失败")
        with allure.step("step3:添加刚创建的特性"):
            res = saveFeature().add_feature(TestCase1.token, product_feature_category, pf_serial)
            pytest.assume(res, "添加特性节点失败")
            TestCase1.added_feature_nodes = res

    @allure.title("结构树添加失效节点--创建失效")
    def test_9(self):
        type0 = TestCase1.dicts["037"][0]["code"]
        type1 = TestCase1.dicts["037"][1]["code"]
        type2 = TestCase1.dicts["037"][2]["code"]
        invalidUseType = f'{type0},{type1},{type2}'  # 失效使用类别
        failureClass = TestCase1.dicts["048"][0]["code"]  # 失效分类
        category = TestCase1.dicts["017"][0]["code"]  # 失效类别
        with allure.step("step1:获取故障模型名称"):
            res = getInvalidModel().get_invalid_model(TestCase1.token, TestCase1.product_type)
            pytest.assume(res, "获取故障模型名称失败")
            faultModeName = res[0]["faultCode"]
        with allure.step("step2:获取功能分组"):
            res = getFunctionGroup().get_function_group(TestCase1.token, TestCase1.product_type)
            functionGroupId = res[0]["groupId"]  # 功能分组ID
        with allure.step("step3:获取产品类别"):
            feature_serial = TestCase1.added_feature_nodes[0]["serialNum"]
            res = selectFeatureProductTypeBySerialNum().select_ft_p_t_by_serial(TestCase1.token, feature_serial)
            pytest.assume(res, "获取产品类别失败")
            product_types = res["productTypes"]
        with allure.step("step4:结构树创建失效"):
            invalid_serial, invalidmode, enInvalidMode = saveInvalid().save_invalid(TestCase1.token,
                                                                                    TestCase1.applicableObject,
                                                                                    category, failureClass,
                                                                                    faultModeName, functionGroupId,
                                                                                    invalidUseType, product_types)
            pytest.assume(invalid_serial, "创建失效失败")
        with allure.step("step5:添加刚创建的失效"):
            pfe_serial = TestCase1.added_feature_nodes[0]["serialNum"]
            ppt_serial = TestCase1.added_product_nodes[0]["serialNum"]
            res = saveInvalid().add_invalid(TestCase1.token, invalid_serial, invalidmode, enInvalidMode, pfe_serial,
                                            ppt_serial)
            pytest.assume(res, "添加失效失败")
            TestCase1.added_invalid_nodes = res

    @allure.title("结构树添加探测措施--创建探测措施")
    def test_10(self):
        with allure.step("step1:获取产品类别"):
            invalid_serial = TestCase1.added_invalid_nodes[0]["serialNum"]
            res = selectInvalidProductTypeBySerialNum().select_i_p_t_by_serial(TestCase1.token, invalid_serial)
            pytest.assume(res, "获取产品类别失败")
            product_types = res["productTypes"]
        with allure.step("step2:新建探测措施"):
            measure_type = TestCase1.dicts["0321"][0]["code"]  # 探测措施分类
            measure_serial, measure, enMeasure = saveMeasure().save_det_measure(TestCase1.token,
                                                                                TestCase1.applicableObject,
                                                                                measure_type, product_types)
            pytest.assume(measure_serial, "创建探测措施失败")
        with allure.step("step3:添加刚创建的探测措施"):
            res = saveMeasure().add_det_measure(TestCase1.token, measure_serial, measure, enMeasure, invalid_serial)
            pytest.assume(res, "添加探测措施失败")

    @allure.title("结构树添加失效原因--创建失效")
    def test_11(self):
        type0 = TestCase1.dicts["037"][0]["code"]
        type1 = TestCase1.dicts["037"][1]["code"]
        type2 = TestCase1.dicts["037"][2]["code"]
        invalidUseType = f'{type0},{type1},{type2}'  # 失效使用类别
        category = TestCase1.dicts["017"][0]["code"]  # 失效类别
        with allure.step("step1:获取产品类别"):
            invalid_serial = TestCase1.added_invalid_nodes[0]["serialNum"]
            res = selectInvalidProductTypeBySerialNum().select_i_p_t_by_serial(TestCase1.token, invalid_serial)
            pytest.assume(res, "获取产品类别失败")
            product_types = res["productTypes"]
        with allure.step("step2:创建失效"):
            serial_number, invalidmode = saveReason().save_reason(TestCase1.token, TestCase1.applicableObject, category,
                                                                  invalidUseType, product_types)
            pytest.assume(serial_number, "创建失效原因失败")

        with allure.step("step3:添加刚创建的失效原因"):
            invalid_obj = TestCase1.added_invalid_nodes[0]
            project_invalids, project_invalid_nets, save_pf_relation = saveReason().add_reason(TestCase1.token,
                                                                                               serial_number,
                                                                                               invalidmode, invalid_obj)
            pytest.assume(project_invalids, "添加失效原因失败")
            pytest.assume(project_invalid_nets, "保存失效网失败")
            pytest.assume(save_pf_relation, "保存功能网失败")
            TestCase1.added_reason_nodes = project_invalids
            TestCase1.save_invalid_nets = project_invalid_nets

    @allure.title("结构树添加预防措施--创建预防措施")
    def test_12(self):
        pre_measure_type = TestCase1.dicts["032"][0]["code"]  # 预防措施分类
        with allure.step("step1:创建预防措施"):
            measure_serial, measure, enMeasure = saveMeasure().save_pre_measure(TestCase1.token,
                                                                                TestCase1.applicableObject,
                                                                                pre_measure_type,
                                                                                TestCase1.product_types)
            pytest.assume(measure_serial, "创建预防措施失败")
        with allure.step("step2:添加刚创建的预防措施"):
            pid_serial = TestCase1.save_invalid_nets[0]["serialNum"]
            pif_serial = TestCase1.save_invalid_nets[0]["pifSerial"]
            res = saveMeasure().add_pre_measure(TestCase1.token, measure_serial, measure, enMeasure, pid_serial,
                                                pif_serial)
            pytest.assume(res, "添加探测措施失败")
