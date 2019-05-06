#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : config.py
# @Date    : 2019-03-20
# @Author  : wudan



import os
# 用例存放路径
current_dir = os.path.dirname(__file__)
case_path = os.path.join(os.path.dirname(current_dir), "test_cases")
#print(case_path)

# 报告存在路径
#report_path = os.path.join(os.path.dirname(current_dir), "reports")
report_path = os.path.join('/home/testing/testcase')
# 日志存放路径
log_path = os.path.join(os.path.dirname(current_dir), "log/test.log")
log_level = 'debug'
# 邮件
mail_path = os.path.join(os.path.dirname(current_dir), "mail")

# source存放路径
test_source = os.path.join(os.path.dirname(current_dir), "test_source")

# history 路径
history_path = os.path.join(os.path.dirname(current_dir), "history")
history_csv = os.path.join(history_path, 'history.csv')
history_html = os.path.join('/home/testing/testcase', 'index.html')
# history_html = os.path.join(history_path, 'index.html')

# gitlog 路径

gitlog_file = os.path.join('/home/testing/cases', 'git.log')
#gitlog_file = os.path.join('D:\\08八卦\\02test', 'git.log')