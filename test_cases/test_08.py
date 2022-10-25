# -*- coding: UTF-8 -*-
import pytest
import allure

from common.get_process_type import getProcessType
from common.get_standard import getStandard
from common.login import Login
from common.get_dict import getDict
from common.get_user_info import getUserInfo
from libs.knowledge.DVP import DVP
from libs.knowledge.det_measure import detMeasure
from libs.knowledge.diagnose_monitor import diagnoseMonitor
from libs.knowledge.element_function import elementFunction
from libs.knowledge.element_invalid import elementInvalid
from libs.knowledge.feature import Feature
from libs.knowledge.frequency_rating import frequencyRating
from libs.knowledge.function_apply import functionApply
from libs.knowledge.functions import Functions
from libs.knowledge.interface import Interface
from libs.knowledge.invalid import Invalid
from libs.knowledge.occ_measure import occMeasure
from libs.knowledge.procedure_element import procedureElement
from libs.knowledge.procedure_function import procedureFunction
from libs.knowledge.process_feature import processFeature
from libs.knowledge.process_procedure import processProcedure
from libs.knowledge.standard import Standard
from libs.knowledge.system_response import systemResponse


class TestCase1:
    token = ""
    user_id = 0
    token2 = ""
    user_id2 = 0
    dicts = {}
    user_info = {}
    product_type = []  # 用户产品类别权限列表
    product_types = []  # 产品类别
    applicableObject = "13e553bc150b4ca58e174ce67dd158cb"  # 适用对象（D）

    def setup_class(self):
        self.user01 = ["cindy3", "Fmeamaster!"]
        self.user02 = ["cindy1", "Fmeamaster!"]

    def teardown_class(self):
        pass

    @allure.title("登录")
    def test_1(self):
        res = Login().login(self.user01)
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

    @allure.title("产品功能库")
    def test_4(self):
        types = [TestCase1.dicts["008"][0]["code"]]  # 功能分类 functionTypes
        customers = [TestCase1.dicts["006"][0]["code"]]  # 客户 customers
        category = TestCase1.dicts["016"][0]["code"]  # 功能类别 functionCategory
        product_types = [TestCase1.product_type[7]]
        with allure.step("step1:选择技术标准"):
            res = getStandard().get_standard(TestCase1.token, TestCase1.product_type)
            standardId = res[0]["standardId"]
            standardNumAndName = f'{res[0]["standardNum"]} {res[0]["standardName"]}'
        with allure.step("step2:创建产品功能"):
            res, function_name = Functions().save_function(TestCase1.token, category, customers, types, product_types,
                                                           standardId,
                                                           standardNumAndName)
            pytest.assume(res["flag"], "创建产品功能失败")
            function_serial = res["serialNum"]
        with allure.step("step3:产品功能下添加失效"):
            res = Functions().add_function_invalid(TestCase1.token, TestCase1.product_type,
                                                   function_serial)
            pytest.assume(res["flag"], "添加失效失败")
        with allure.step("step4:删除产品功能下的失效"):
            res = Functions().del_function_invalid(TestCase1.token, TestCase1.product_type, function_name)
            pytest.assume(res["flag"], "删除产品功能下的失效失败")
        with allure.step("step5:删除产品功能"):
            res = Functions().del_function(TestCase1.token, function_serial)
            pytest.assume(res["flag"], "删除产品功能失败")

    @allure.title("界面功能库")
    def test_5(self):
        type = TestCase1.dicts["009"][0]["code"]  # 界面类别
        with allure.step("step1:创建界面功能"):
            res = Interface().save_interface(TestCase1.token, type)
            pytest.assume(res["flag"], "创建技术标准失败")
            IF_serial = res["serialNum"]
        with allure.step("step2:删除界面功能"):
            res = Interface().del_interface(TestCase1.token, IF_serial)
            pytest.assume(res["flag"], "删除界面功能失败")

    @allure.title("技术标准库")
    def test_6(self):
        standardType = TestCase1.dicts["012"][0]["code"]  # 标准类型
        obj = TestCase1.product_type[7]
        customer = TestCase1.dicts["006"][0]["code"]  # 客户 customer
        with allure.step("step1:创建技术标准"):
            res = Standard().save_standard(TestCase1.token, customer, standardType, obj)
            pytest.assume(res["flag"], "创建技术标准失败")
            standard_serial = res["serialNum"]
        with allure.step("step2:删除技术标准"):
            res = Standard().del_standard(TestCase1.token, standard_serial)
            pytest.assume(res["flag"], "删除技术标准失败")

    @allure.title("产品特性库")
    def test_7(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        with allure.step("step1:创建产品特性"):
            res = Feature().save_feature(TestCase1.token, product_types)
            pytest.assume(res["flag"], "创建特性失败")
            feature_serial = res["serialNum"]
        with allure.step("step2:删除产品特性"):
            res = Feature().del_feature(TestCase1.token, feature_serial)
            pytest.assume(res["flag"], "删除产品特性失败")

    @allure.title("产品失效库")
    def test_8(self):
        type0 = TestCase1.dicts["037"][0]["code"]
        type1 = TestCase1.dicts["037"][1]["code"]
        type2 = TestCase1.dicts["037"][2]["code"]
        invalidUseType = f'{type0},{type1},{type2}'  # 失效使用类别
        failureClass = TestCase1.dicts["048"][0]["code"]  # 失效分类
        category = TestCase1.dicts["017"][0]["code"]  # 失效类别
        product_types = [TestCase1.product_type[7]]
        with allure.step("step1:获取故障模型名称"):
            res = Invalid().get_fault_mode(TestCase1.token)
            pytest.assume(res, "获取故障模型名称失败")
            pytest.assume(len(res) > 0, "故障模型名称数据空")
            faultModeName = res[0]["faultCode"]
        with allure.step("step2:获取功能分组"):
            res = Invalid().get_function_group(TestCase1.token)
            pytest.assume(res, "获取功能分组失败")
            pytest.assume(len(res) > 0, "功能分组数据空")
            functionGroupId = res[0]["groupId"]  # 功能分组ID
        with allure.step("step3:创建产品失效"):
            res, invalidmode = Invalid().save_invalid(TestCase1.token, TestCase1.applicableObject, category,
                                                      failureClass,
                                                      faultModeName,
                                                      functionGroupId, invalidUseType, product_types)
            pytest.assume(res, "创建产品失效失败")
            invalid_serial = res
        with allure.step("step4:产品失效下添加措施"):
            res = Invalid().add_invalid_measure(TestCase1.token, invalid_serial, TestCase1.product_type)
            pytest.assume(res["flag"], "产品失效下添加措施失败")
        with allure.step("step5:删除产品失效下的措施"):
            res = Invalid().delete_invalid_measure(TestCase1.token, TestCase1.product_type, invalidmode)
            pytest.assume(res["flag"], "删除产品失效下的措施失败")
        with allure.step("step6:删除产品失效"):
            res = Invalid().del_invalid(TestCase1.token, invalid_serial)
            pytest.assume(res["flag"], "删除产品失效失败")

    @allure.title("预防措施库")
    def test_9(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        pre_measure_type = TestCase1.dicts["032"][0]["code"]  # 预防措施分类
        with allure.step("step1:创建预防措施"):
            res = occMeasure().save_occ_measure(TestCase1.token, TestCase1.applicableObject, pre_measure_type,
                                                product_types)
            pytest.assume(res["flag"], "创建预防措施失败")
            occ_measure_serial = res["serialNum"]
        with allure.step("step2:删除预防措施"):
            res = occMeasure().del_occ_measure(TestCase1.token, occ_measure_serial)
            pytest.assume(res["flag"], "删除预防措施失败")

    @allure.title("探测措施库")
    def test_10(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        reactionPlan = TestCase1.dicts["038"][0]["code"]  # 反应计划
        type = TestCase1.dicts["0321"][0]["code"]  # 措施分类
        with allure.step("step1:创建探测措施"):
            res = detMeasure().save_det_measure(TestCase1.token, TestCase1.applicableObject, reactionPlan, type,
                                                product_types)
            pytest.assume(res["flag"], "创建探测措施失败")
            det_measure_serial = res["serialNum"]
        with allure.step("step2:删除探测措施"):
            res = detMeasure().del_det_measure(TestCase1.token, det_measure_serial)
            pytest.assume(res["flag"], "删除探测措施失败")

    @allure.title("频率评级措施")
    def test_11(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        with allure.step("step1:创建频率评级措施"):
            res = frequencyRating().save_frequency_rating(TestCase1.token, product_types)
            pytest.assume(res["flag"], "创建频率评级措施失败")
            frequency_measure_serial = res["serialNum"]
        with allure.step("step2:删除频率评级措施措施"):
            res = frequencyRating().del_frequency_rating(TestCase1.token, frequency_measure_serial)
            pytest.assume(res["flag"], "删除频率评级措施失败")

    @allure.title("诊断监视措施")
    def test_12(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        with allure.step("step1:创建诊断监视措施"):
            res = diagnoseMonitor().save_diagnose_monitor(TestCase1.token, product_types)
            pytest.assume(res["flag"], "创建诊断监视措施失败")
            diagnose_measure_serial = res["serialNum"]
        with allure.step("step2:删除诊断监视措施"):
            res = diagnoseMonitor().del_diagnose_monitor(TestCase1.token, diagnose_measure_serial)
            pytest.assume(res["flag"], "删除诊断监视措施失败")

    @allure.title("系统响应措施")
    def test_13(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        with allure.step("step1:创建系统响应措施"):
            res = systemResponse().save_system_response(TestCase1.token, product_types)
            pytest.assume(res["flag"], "创建系统响应措施失败")
            system_response_serial = res["serialNum"]
        with allure.step("step2:删除系统响应措施"):
            res = systemResponse().del_system_response(TestCase1.token, system_response_serial)
            pytest.assume(res["flag"], "删除系统响应措施失败")

    @allure.title("DVP")
    def test_14(self):
        dvpLayer = TestCase1.dicts["004"][0]["code"]  # 实验层级
        product_types = TestCase1.product_type[7]  # 获取一个产品类别
        with allure.step("step1:创建DVP"):
            flag, dvpName = DVP().save_DVP(TestCase1.token, dvpLayer, product_types)
            pytest.assume(flag, "创建DVP失败")
        with allure.step("step2:查询刚创建的DVP，获取serialNum"):
            res = DVP().search_DVP(TestCase1.token, TestCase1.product_type, dvpName)
            pytest.assume(len(res) > 0, "查询结果为空")
            DVP_serial = res[0]["serialNum"]
        with allure.step("step3:删除DVP"):
            res = DVP().del_DVP(TestCase1.token, DVP_serial)
            pytest.assume(res["flag"], "删除DVP失败")

    @allure.title("过程工序")
    def test_15(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        with allure.step("step1:获取工序分类"):
            res = getProcessType().get_process_type(TestCase1.token)
            pytest.assume(len(res) > 0, "工序分类列表为空")
            procedureType = res[0]["code"]
        with allure.step("step2:创建过程工序"):
            res = processProcedure().save_process_procedure(TestCase1.token, procedureType, product_types)
            pytest.assume(res["flag"], "创建过程工序失败")
            pp_serial = res["serialNum"]
        with allure.step("step3:删除过程工序"):
            res = processProcedure().del_process_procedure(TestCase1.token, pp_serial)
            pytest.assume(res["flag"], "删除过程工序失败")

    @allure.title("工序功能")
    def test_16(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        types = TestCase1.dicts["008"][0]["code"]  # 功能分类 functionTypes
        category = TestCase1.dicts["016"][0]["code"]  # 功能类别 functionCategory
        with allure.step("step1:创建工序功能"):
            res = procedureFunction().save_procedure_fun(TestCase1.token, types, category, product_types)
            pytest.assume(res["flag"], "创建工序功能失败")
            pf_serial = res["serialNum"]
        with allure.step("step2:删除工序功能"):
            res = procedureFunction().del_procedure_fun(TestCase1.token, pf_serial)
            pytest.assume(res["flag"], "删除工序功能失败")

    @allure.title("工序要素")
    def test_17(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        elementType = TestCase1.dicts["014"][0]["code"]  # 要素类型 elementType
        with allure.step("step1:创建工序要素"):
            res = procedureElement().save_procedure_element(TestCase1.token, elementType, product_types)
            pytest.assume(res["flag"], "创建工序要素失败")
            pe_serial = res["serialNum"]
        with allure.step("step2:删除工序要素"):
            res = procedureElement().del_procedure_element(TestCase1.token, pe_serial)
            pytest.assume(res["flag"], "删除工序要素失败")

    @allure.title("要素功能")
    def test_18(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        elementType = TestCase1.dicts["014"][0]["code"]  # 要素类型 elementType
        category = TestCase1.dicts["016"][0]["code"]  # 功能类别 functionCategory
        with allure.step("step1:创建要素功能"):
            res = elementFunction().save_element_function(TestCase1.token, category, elementType, product_types)
            pytest.assume(res["flag"], "创建要素功能失败")
            ef_serial = res["serialNum"]
        with allure.step("step2:删除要素功能"):
            res = elementFunction().del_element_function(TestCase1.token, ef_serial)
            pytest.assume(res["flag"], "删除要素功能失败")

    @allure.title("要素失效")
    def test_19(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        elementType = TestCase1.dicts["014"][0]["code"]  # 要素类型 elementType
        with allure.step("step1:创建要素失效"):
            res = elementInvalid().save_element_invalid(TestCase1.token, elementType, product_types)
            pytest.assume(res["flag"], "创建要素失效失败")
            ei_serial = res["serialNum"]
        with allure.step("step2:删除要素失效"):
            res = elementInvalid().del_element_invalid(TestCase1.token, ei_serial)
            pytest.assume(res["flag"], "删除要素失效失败")

    @allure.title("过程特性库")
    def test_20(self):
        product_types = [TestCase1.product_type[7]]  # 获取一个产品类别
        elementType = TestCase1.dicts["014"][0]["code"]  # 要素类型 elementType
        with allure.step("step1:创建过程特性"):
            res = processFeature().save_process_feature(TestCase1.token, elementType, product_types)
            pytest.assume(res["flag"], "创建过程特性")
            pc_serial = res["serialNum"]
        with allure.step("step2:删除过程特性"):
            res = processFeature().del_process_feature(TestCase1.token, pc_serial)
            pytest.assume(res["flag"], "删除过程特性失败")

    @allure.title("产品功能审核")
    def test_21(self):
        types = [TestCase1.dicts["008"][0]["code"]]  # 功能分类 functionTypes
        product_types = [TestCase1.product_type[7]]
        with allure.step("step1:创建产品功能"):
            res, function_name = Functions().save_function(TestCase1.token, "", [], types, product_types, "", "")
            pytest.assume(res["flag"], "创建产品功能失败")
            function_serial = res["serialNum"]
        with allure.step("step2:提交审核"):
            res = functionApply().function_apply(TestCase1.token, self.user01[0], function_serial, function_name,
                                                 TestCase1.product_type)
            pytest.assume(res["flag"], "提交审核失败")
        with allure.step("step3:审核同意"):
            res = Login().login(self.user02)
            pytest.assume(res, "登录失败")
            TestCase1.token2 = res["token"]
            res = functionApply().function_approve(TestCase1.token2, self.user01[0], function_serial, function_name,
                                                   TestCase1.product_type)
            pytest.assume(res["flag"], "审核同意失败")
        with allure.step("step4:删除产品功能"):
            res = Functions().del_function(TestCase1.token, function_serial)
            pytest.assume(res["flag"], "删除产品功能失败")
