#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : get_output_key.py
# @Date    : 2019-03-19
# @Author  : wudan

import io
import json
import os
import logging
from .IdToChinese import IdToChinese



class ApproveOutput:
    def __init__(self):
        """
        :param case_path: 输入测试用例目录
        :self.case_path: 测试用例的绝对路径
        :self.case_json: 测试用例中json文件路径
        :self.case_image:测试用例中images文件路径
        :self.num_name:测试用例的项目编号
        :self.chi_name:测试用例的中文名字
        :self.audioResult: json输出所有结果数组
        :self.approval_information:输出json中规则数组
        :self.docs:输出json中文档分类结果数据
        :self.classify_four_w:输出json中的4W分类数组
        :self.key_miss:输出json文件中是否缺失键
        """
        self.case_path = ''
        self.case_json = ''
        self.case_image = ''
        self.num_name = ''
        self.chi_name = ''

        self.audioResult = []
        self.approval_information = []
        self.docs = []
        self.classify_four_w = []

        self.actual_audioResult = []
        self.actual_docs = []
        self.actual_four_w = []
        self.actual_approval_information = []

        self.key_miss = False
        self.miss_messages = []
        # self.output_key['docs'] = ['testflag', 'seq', 'imageUrl', 'approvalDocumentId', 'audioDocumentId', 'docName']
        # self.output_key['four_w'] = ['rotation_angle', 'form_typeid', 'field_content', 'imageUrl','document_field', 'document_name', 'field_location', 'document_id']

    def get_output_json(self, case_path):
        """
        1.extract the key of the output json files
        2.return whether there are keys missed.
        :param path: input is the path of cases output json files
        :return:
        """
        if not os.path.exists(case_path):
            logging.ERROR('the path of source files does not exist')
        else:
            self.case_path = os.path.abspath(case_path)
            self.case_json = os.path.join(self.case_path, 'output.json')
            self.case_image = os.path.join(self.case_path, 'images')
            self.num_name = os.path.abspath(self.case_path).split(sep='\\')[-2]
            self.chi_name = IdToChinese[self.num_name]

        with io.open(self.case_json, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            self.audioResult = json_data['data']['audioResult']
            self.docs = self.audioResult['docs']
            self.classify_four_w= self.audioResult['4W']
            self.approval_information = self.audioResult['approval_information']
        return True

    def audioResult_miss_key(self):
        """
        测试audioResult是否缺失键
        如果缺失，则打印缺失的键
        返回值为打印信息
        """
        self.key_miss = False
        audioResult_keys = {
            'ticketMd5': 0,
            'audioRecordId': 0,
            'ticketId': 0,
            'identityNumber': 0,
            'docs': 0,
            'approval_information': 0,
            '4W': 0
        }

        self.miss_messages = []
        if self.audioResult:
            for key in self.audioResult.keys():
                if key in audioResult_keys:
                    audioResult_keys[key] += 1

            for key, count in audioResult_keys.items():
                if count is 0 :
                    self.key_miss = True
                    self.miss_messages.append("【{}】-【audioResult】- 丢失键 【{}】".format(self.num_name,key))
        else:
            self.miss_messages.append('【{}】-【audioResult】-没有键'.format(self.num_name))
        return self.miss_messages

    def docs_miss_key(self):
        """
        测试文档是否有缺失键
        如果缺失，则打印缺失的键
        返回值为打印信息
        """
        self.key_miss = False
        self.miss_messages = []
        doc_num = 0
        if self.docs:
            for doc_json in self.docs:
                docs_keys = {
                    'testflag': 0,
                    'seq': 0,
                    'imageUrl': 0,
                    'approvalDocumentId': 0,
                    'audioDocumentId': 0,
                    'docName': 0
                }
                for key in doc_json:
                    if key in docs_keys:
                        docs_keys[key] += 1

                for key, count in docs_keys.items():
                    if count is 0:
                        self.key_miss = True
                        self.miss_messages.append("【{}】-【docs】-【{}】-丢失键-【{}】".format(self.num_name, doc_num, key))
                doc_num += 1

        else:
            self.key_miss = True
            self.miss_messages.append('【{}】-【docs】没有键'.format(self.num_name))
        return self.miss_messages

    def classify_four_w_miss_key(self):
        """
        测试four_w归类是否有缺失键
        如果缺失，则打印缺失的键
        返回值为打印信息
        """
        self.key_miss = False
        self.miss_messages = []
        classify_four_w_keys = {
            'WHO' : 0,
            'SIGN': 0,
            'WHEN': 0,
            'WHAT' : 0,
            'OTHER': 0,
            'WHERE': 0,
            'COPY_ID': 0
        }
        if self.classify_four_w:
            for four_w in self.classify_four_w:
                if four_w in classify_four_w_keys:
                    classify_four_w_keys[four_w] += 1
            """判断4W分类是否丢失 WHO，SIGN，WHEN，WHAT，OTHER，WHERE，COPY_ID"""
            for key, count in classify_four_w_keys.items():
                if count is 0:
                    self.key_miss = True
                    self.miss_messages.append("【{}】-【4W分类】- 丢失键-【{}】".format(self.num_name,key))

            for four_w, four_w_value in self.classify_four_w.items():
                # classify_four_w_subkeys = {
                #     'name': 0,
                #     'content': 0
                # }
                # print(four_w, four_w_value)
                four_w_num = 0
                for sub_four_w in four_w_value:
                    """ 判断4W分类是否丢失 name ，content键"""
                    if 'name' not in sub_four_w.keys():
                        self.key_miss = True
                        self.miss_messages.append("【{}】-【4W分类】-【{}】-【{}】- 丢失键-【name】".format(self.num_name, four_w, four_w_num))
                    """判断4W分类 content子键里是否丢失 键"""
                    if 'content' in sub_four_w.keys():
                        content_num = 0
                        for content_key in sub_four_w['content']:
                            classify_four_w_content_keys = {
                                'rotation_angle': 0,
                                'document_field': 0,
                                'field_location': 0,
                                'document_id': 0,
                                'field_content': 0,
                                'form_typeid': 0,
                                'document_name': 0,
                                'imageUrl': 0
                            }
                            for content_subkey in content_key.keys():
                                if content_subkey in classify_four_w_content_keys:
                                    classify_four_w_content_keys[content_subkey] +=1
                            for subkey, count in classify_four_w_content_keys.items():
                                if count is 0 :
                                    self.key_miss = True
                                    self.miss_messages.append("【{}】-【4W分类】-【{}】-【{}】-【content】- 丢失键 - 【{}】".format(self.num_name, four_w, four_w_num, subkey))
                        content_num += 1
                    else:
                        self.key_miss = True
                        self.miss_messages.append(
                            "{}4W分类 -【{}】-【{}】- 丢失键 【content】".format(self.num_name, four_w, four_w_num))
                    four_w_num += 1
        else:
            self.key_miss = True
            self.miss_messages.append('【{}】-【docs】没有键'.format(self.num_name))
        return self.miss_messages

    def approval_information_miss_key(self):
        self.key_miss = False
        self.miss_messages = []
        if self.approval_information:
            approval_num = 0
            for approval in self.approval_information:
                # print(approval)
                approval_keys = {
                    'approval_basis': 0,
                    'approval_point': 0,
                    'approval_point_id': 0,
                    'approval_result': 0,
                    'document_and_field': 0,
                    'law_basis': 0,
                    'main_doc_id': 0
                }

                for key in approval.keys():
                    if key in approval_keys:
                        approval_keys[key] += 1
                for app_key, count in approval_keys.items():
                    if count is 0:
                        self.key_miss = True
                        self.miss_messages.append("【{}】-【规则结果approval_information】-【{}】-丢失键-【{}】".format(self.num_name, approval_num, app_key))
                if approval['document_and_field']:
                    field_num = 0
                    field_keys = {
                        'document_field': 0,
                        'document_id': 0,
                        'field_content': 0,
                        'seq': 0,
                        'document_name': 0,
                        'field_location': 0,
                        'rotation_angle': 0,
                        'imageUrl': 0
                    }
                    for field in approval['document_and_field']:
                        # print(field)
                        for field_subkey in field:
                            if field_subkey in field_keys:
                                field_keys[field_subkey] += 1
                        for key, count in field_keys.items():
                            if count is 0:
                                self.key_miss = True
                                self.miss_messages.append("【{}】-【规则结果approval_information】-【{}】-【document_and_field】-【{}】- 丢失键-【{}】".format(self.num_name, approval_num, field_num, key))
                        field_num += 1

                approval_num += 1
        return self.miss_messages






#   def is_key_missed(self):


if __name__ == '__main__':
    case1 = ApproveOutput()
    case1.get_output_json(os.path.abspath('D:\\08八卦\\02test\\AutoTest\\source\\test\\SH00PD_959201101\\case1'))
    print(case1.docs_miss_key())
    # if 'rotation_angle' in case1.audioResult.key:
    #
    # print(case1.audioResult.has_key('rotation_angle'))