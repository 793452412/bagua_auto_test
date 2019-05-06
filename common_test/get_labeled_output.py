#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : get_labeled_output.py
# @Date    : 2019-03-21
# @Author  : wudan

import os
import io
import json
from config import config
from common_test.IdToChinese import IdToChinese

class SampleSystemOutput:
    """样例生成系统的json"""

    def __init__(self, source_path, case_num):
        """
        :param source_path: 事项目录
        :param case_num: 样本序号
        """
        # 判断事项是否存在
        if source_path in IdToChinese:
            self.case_name = source_path
            self.chinese_name = IdToChinese[source_path]
        # 判断事项人工标定的json是否存在，如果不存在，则退出测试
        json_file = os.path.join(config.test_source, source_path , case_num, "expected_json.json")
        if os.path.exists(json_file):
            with open(json_file, 'r+', encoding= 'utf-8') as f:
                self.expected_json = json.load(f)
                self.docs = self.expected_json['docs']
                self.rules = self.expected_json['rules']
                self.fields = self.expected_json['fields']
        else:
            #print(json_file)
            self.expected_json = []
            print('no files')

    def docs_labeled(self):
        for docs in self.docs:
            is_exist = False
            for pic in self.docs_set:
                if docs['picture_name'] == pic['picture_name']:
                    is_exist = True
                    break
            if is_exist is not True:
                self.docs_set.append(docs)
        #print(self.docs_set)

    def approval_result_labeled(self):
        self.rules = self.expected_json['rules']



if __name__ == '__main__':
    case = SampleSystemOutput("SH00PD_963201101",'case1')
    #case.docs_labeled()
    case.approval_result_labeled()
    print(case.docs)