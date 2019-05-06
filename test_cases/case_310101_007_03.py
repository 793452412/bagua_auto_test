#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : case1_SH00PD_959201101.py
# @Date    : 2019-03-20
# @Author  : wudan

import common_test.get_output_key
import os
from common_test.get_output_key import ApproveOutput
from common_test.get_labeled_output import *
from common_test.IdToChinese import *
from common_test.mylogging import *
from common_test.get_output import *
from common_test.common_compare import *
from HTMLTestRunner_PY3.HTMLTestRunner_PY3 import HTMLTestRunner

case_path = os.path.abspath('./test_source/310101-007-03')
case_num = 'case1'
case_num_path = os.path.join(case_path, case_num)
images_path = os.path.join(case_path, case_num, 'images')
results_path = os.path.join(case_path, case_num, 'output.json')

import unittest


#class test_310101_007_03(unittest.TestCase):
class PudongTest(unittest.TestCase):
    """变更（食品经营许可证）"""
    # @classmethod
    # def setUpClass(cls):
    #     input_config = {'config': '''{"sid":"310101-007-03","description":"内资新设",audioRecordId:""}'''}
    #     auto_record_id = input_url(input_config, case_num_path)
    #     cls.assertIsNotNone(auto_record_id, '无法获取当前记录ID')
    #     if auto_record_id:
    #         output = output_url(auto_record_id, results_path)
    #     cls.assertIsNotNone(output, '无法获取当前程序输出json')


    def test_310101_007_03_case1(self):
        """CASE-1"""
        input_config = {'config': '''{"sid":"310101-007-03","description":"内资新设",audioRecordId:""}'''}
        self.auto_record_id = input_url(input_config, case_num_path)
        self.assertIsNotNone(self.auto_record_id, '无法获取当前记录ID')
        if self.auto_record_id:
            self.output = output_url(self.auto_record_id, results_path)
        self.assertIsNotNone(self.output, '无法获取当前程序输出json')
        # 添加具体的程序
        # with open(results_path, "r+", encoding='UTF-8') as f:
        #    self.output = json.load(f)
        self.sample = SampleSystemOutput(case_path, case_num)
        # self.sample.docs_labeled()
        self.docs = self.output['data']['docs']
        self.rules = self.output['data']['approval_information']
        self.fields = self.output['data']['docs']
        """测试文档分类结果"""
        print('\n****************测试文档分类结果***********************\n')
        error_doc = docs_sorted_compare(self.sample.docs, self.docs)
        if error_doc:
            print("文档分类有错误")
            error = True
        """测试规则结果和描述"""
        print('\n****************测试规则结果和描述**********************\n')
        error_rule = rules_compare(self.sample.rules, self.rules)
        if error_rule:
            print("规则审批有错误")
            error = True
        self.assertFalse(error, msg="样本测试失败")

    def test_310101_007_03_case2(self):
        """CASE-2"""
        print('123')
        self.assertFalse(False)

    def test_310101_007_03_case3(self):
        self.assertFalse(False)


    # def test_get_ouputjson_from_platform(self):
    #     """直接读取output.json"""
    #     with open(results_path, "r+",encoding='UTF-8') as f:
    #         self.output = json.load(f)
    #     self.sample = SampleSystemOutput(case_path, case_num)
    #     # self.sample.docs_labeled()
    #     self.docs = self.output['data']['docs']
    #     self.rules = self.output['data']['approval_information']
    #     self.fields = self.output['data']['docs']
    #
    # def test_docs_sorted(self):
    #     """测试文档分类结果"""
    #     error = docs_sorted_compare(self.sample.docs, self.docs)
    #     self.assertFalse(error, msg= "文档分类有错误")
    #
    # def test_rules_results(self):
    #     """测试规则结果和描述"""
    #     error = rules_compare(self.sample.rules, self.rules)
    #     self.assertFalse(error, msg= "规则审批有错误")
    #
    # @unittest.expectedFailure
    # def test_rules_results_knownissue(self):
    #     known_skip = rules_compare_knownissue(self.sample.rules, self.rules)
    #     self.assertFalse(known_skip, msg= "规则审批错误可忽略")
    #
    # @unittest.expectedFailure
    # def test_docs_sorted_compare_knownissue(self):
    #     known_skip = docs_sorted_compare_knownissue(self.sample.docs, self.docs)
    #     self.assertFalse(known_skip, msg= "文档分类错误可忽略")


if __name__ == '__main__':
    test_suite = unittest.TestSuite()  # 创建一个测试集合
    # test_suite.addTest(MyTest('test_get_ouputjson_from_platform_0'))
    # test_suite.addTest(MyTest('test_docs_sorted_2'))  # 测试套件中添加测试用例

    test_suite.addTest(unittest.makeSuite(CaseOne)) #使用makeSuite方法添加所有的测试方法
    test_suite.addTest(unittest.makeSuite(CaseTwo))
    fp = open('res_report_1.html', 'wb')  # 打开一个保存结果的html文件
    runner = HTMLTestRunner(stream=fp, title='浦东人工智能辅助审批事项测试报告')
    # 生成执行用例的对象
    result = runner.run(test_suite)

    # 执行测试套件
    #unittest.main()

