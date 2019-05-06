#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : common_compare.py
# @Date    : 2019-04-11
# @Author  : wudan

from config.config import *


def docs_sorted_compare(label_docs, output_docs):
    """
    :param label_docs: 真值doc
    :param output_docs: 测试值doc
    :return: error 是否有错误
    """
    error = False
    # print(label_docs_set, output_docs)
    if label_docs and output_docs:
        for doc in output_docs:
            # print(doc['originalName'])
            is_necessary = False
            for pic in label_docs:
                if doc['originalName'] == pic['picture_name']:
                    is_necessary = True
                    # print(doc.keys())
                    if str(doc['seq']) == str(pic['seq']):
                        print("{}分类结果是{}，与预期{}相符".format(doc['originalName'], doc['seq'], pic['seq']))
                    else:
                        error = True
                        print("【error】{}分类结果是{}，与预期{} 不符".format(doc['originalName'], doc['seq'], pic['seq']))
                    break
                else:
                    continue
            # print(is_necessary)
            if is_necessary is False:
                if str(doc['seq']) == '0':
                    error = False
                    print("{}分类结果是 0 ，为非必需材料".format(doc['originalName']))
    else:
        error = True
        print('docs字段没有内容')
    return error


def docs_sorted_compare_knownissue(label_docs, output_docs):
    """
    :param label_docs: 真值doc
    :param output_docs: 测试值doc
    :return: 是否可忽略
    """
    error = False
    error_num = 0
    known_fail = False
    # print(label_docs_set, output_docs)
    if label_docs and output_docs:
        for doc in output_docs:
            # print(doc['originalName'])
            is_necessary = False
            for pic in label_docs:
                if doc['originalName'] == pic['picture_name']:
                    is_necessary = True
                    # print(doc.keys())
                    if str(doc['seq']) == str(pic['seq']):
                        print("{}分类结果是{}，与预期{}相符".format(doc['originalName'], doc['seq'], pic['seq']))
                    else:
                        error = True
                        error_num += 1
                        print("【error】{}分类结果是{}，与预期{} 不符".format(doc['originalName'], doc['seq'], pic['seq']))
                        if pic['IsKnown'] == '是':
                            error_num -= 1

                    break
                else:
                    continue
            # print(is_necessary)
            if is_necessary is False:
                if int(doc['seq']) == 0:
                    error = False
                    print("{}分类结果是 0 ，为非必需材料".format(doc['originalName']))
    else:
        error = True
        error_num += 1
        print('docs字段没有内容')
    if error:
        if error_num == 0:
            known_fail = True
        else:
            known_fail = False
    else:
        known_fail = True
    return known_fail


def rules_compare(label_rules, output_rules):
    """
    :param label_rules: 真值rule
    :param output_rules: 测试值rule
    :return: 是否有error
    """
    error = False
    if label_rules and output_rules:
        # print(label_rules, output_rules)
        for rule in output_rules:
            # print(doc['originalName'])
            is_same = False
            for srule in label_rules:
                if int(rule['approval_point_id']) == int(srule['RuleID']):
                    is_same = True
                    if rule['approval_result'] == srule['ResultsLabeled'] and rule['approval_basis'] == srule[
                        'NoteLabeled']:
                        print("【pass】【{}】 审批结果是{}，与预期相符;审批描述是{},与预期相符".format(rule['approval_point_id'],
                                                                              rule['approval_result'],
                                                                              rule['approval_basis']))
                    else:
                        error = True
                        if rule['approval_result'] is not srule['ResultsLabeled']:
                            print(
                                "【error】【{}】审批结果是{}，与预期{} 不符".format(rule['approval_point_id'], rule['approval_result'],
                                                                     srule['ResultsLabeled']))
                        if rule['approval_basis'] is not srule['NoteLabeled']:
                            print("【error】【{}】审批结果描述是{}，与预期{} 不符".format(rule['approval_point_id'],
                                                                         rule['approval_basis'],
                                                                         srule['NoteLabeled']))
                    break
                else:
                    continue
            # print(is_necessary)
            if is_same is False:
                error = True
                print("【error】【{}】没有找到人工标定记录".format(rule['approval_point_id']))
    else:
        error = True
        print('rule字段没有内容')
    return error


def rules_compare_knownissue(label_rules, output_rules):
    """
    :param label_rules: 真值rule
    :param output_rules: 测试值rule
    :return: 是否预期失败
    """
    error = False
    error_num = 0
    known_issue = False
    if label_rules and output_rules:
        # print(label_rules, output_rules)
        for rule in output_rules:
            # print(doc['originalName'])
            is_same = False
            for srule in label_rules:
                if str(rule['approval_point_id']) == str(srule['RuleID']):
                    is_same = True
                    if rule['approval_result'] == srule['ResultsLabeled'] and rule['approval_basis'] == srule[
                        'NoteLabeled']:
                        print("【pass】【{}】 审批结果是{}，与预期相符;审批描述是{},与预期相符".format(rule['approval_point_id'],
                                                                              rule['approval_result'],
                                                                              rule['approval_basis']))
                    else:
                        error = True
                        error_num += 1
                        if rule['approval_result'] is not srule['ResultsLabeled']:
                            print(
                                "【error】【{}】审批结果是{}，与预期{} 不符".format(rule['approval_point_id'], rule['approval_result'],
                                                                     srule['ResultsLabeled']))
                        if rule['approval_basis'] is not srule['NoteLabeled']:
                            print("【error】【{}】审批结果描述是{}，与预期{} 不符".format(rule['approval_point_id'],
                                                                         rule['approval_basis'],
                                                                       srule['NoteLabeled']))
                        if srule['IsKnown'] == '是':
                            known_issue = True
                            error_num -= 1
                    break
                else:
                    continue
            # print(is_necessary)
            if is_same is False:
                error = True
                error_num += 1
                print("【error】【{}】没有找到人工标定记录".format(rule['approval_point_id']))
    else:
        error = True
        error_num += 1
        print('rule字段没有内容')

    if error:
        if error_num == 0:
            known_fail = True
        else:
            known_fail = False
    else:
        known_fail = True
    return known_fail





