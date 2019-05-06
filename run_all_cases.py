#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : run_all_cases.py
# @Date    : 2019-03-20
# @Author  : wudan
import pandas as pd
import os
import time
import unittest
from config.config import *
from HTMLTestRunner_PY3.HTMLTestRunner_PY3 import *
from mail.ReportMail import *
from common_test.mylogging import *

def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="case_*.py")
    print(case_path)
    print(discover)
    return discover


def update_history_csv(his_path, result ,binary_link):
    """
    :param his_path: 存放history.csv路径
    :param result: 测试结果
    :param binary_link: commit id
    :return: history pandas
    """
    with open(his_path, 'rb') as f:
        df_history = pd.read_csv(f)

    # print(df_history)
    result_dic = {
        'date': [time.strftime('%Y-%m-%d', time.localtime(time.time()))],
        'report_name': [time.strftime('%Y%m%d', time.localtime(time.time())) + 'Report.html'],
        'binary_link': [binary_link],
        'run_time': [str(runner.startTime)],
        'total_cases': [runner.case_num],
        'Pass': [runner.case_pass],
        'fail': [runner.case_fail],
        'ignore': [runner.case_ignore],
        'unignore': [runner.case_unignore],
        'error': [runner.case_err]
    }
    #print(type(result_dic['Pass']))
    new = pd.DataFrame(data=result_dic)
    # print(new)
    df_history = df_history.append(new, ignore_index=True)
    # print(df_history)
    df_history.sort_values('run_time',ascending = False, inplace = True)
    df_history.reset_index(drop= True, inplace = True)
    # print(df_history)
    df_history.to_csv(his_path, index=False)
    return df_history

def get_binary_link(gitlog_path):
    """
    :param gitlog_path: gitlog文件目录
    :return: 返回当前最新程序git commit id
    """
    if os.path.exists(gitlog_path):
        with open(gitlog_path, 'r+') as f:
            for line in f:
                binary_link = line
    else:
        print("找不到git.log文件")
    print(type(binary_link))
    return binary_link



if __name__ == "__main__":
    # 实例化TextTestRunner类
    # runner = unittest.TextTestRunner()
    # 使用run()方法运行测试套件（即运行测试套件中的所有用例）

    report_file = os.path.join(report_path, time.strftime('%Y%m%d',time.localtime(time.time()))+'Report.html')
    fp = open(report_file, 'wb')
    # 打开一个保存结果的html文件
    runner = HTMLTestRunner(stream=fp, title='浦东人工智能辅助审批事项测试报告')
    result = runner.run(all_case())
    print(result)

    fp_his = open(history_html, 'wb')
    his = HtmlHistory(fp_his)
    binary_link = get_binary_link(gitlog_file)
    df_history = update_history_csv(history_csv, runner, str(binary_link))
    his.generate_history_html(df_history)
    testReport_mail(report_file,runner)


