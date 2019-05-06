#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : get_output.py
# @Date    : 2019-04-09
# @Author  : wudan

import os
import io
import json
import sys
from config.config import *
from common_test.IdToChinese import IdToChinese
import time
import requests
from common_test.mylogging import *



def eachFile(filepath):
    files = []
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join(filepath, allDir)
        log.logger.info("添加测试图片{}".format(allDir))
        tup = ('file', open(child,'rb'))
        files.append(tup)
    return files


def input_url(input_config, case_path):
    """
    :param inputConfig: dictionary
    config = {"sid":"SH00PD_963201101","description":"内资新设",audioRecordId:""}
    file = eachFile(filepath)
    :return: audioRecordId
    """
    res = {}
    audioRecordId = ""
    time_out = False
    images_path = os.path.join(case_path, 'images')
    files = eachFile(images_path)

    input_json = os.path.join(case_path, "input.json")
    log.logger.info("*******************************************************")
    log.logger.info("正在访问接口/sjtu/api/test/buildInputAndSent，请稍等")
    url_time = 0
    url = 'http://10.50.12.46:9001/sjtu/api/test/buildInputAndSent'
    #log.logger.info("input中的接口输入;\ndata=%s\nfiles=%s"%(json.dumps(input_config, ensure_ascii=False),files))
    # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    # inputData['files']  = files
    sys.stdout.flush()
    while True:
        r = requests.post(url, data=input_config, files = files)
        sys.stdout.flush()
        time.sleep(5)
        # log.logger.info r.elapsed.microseconds
        url_time += 5
        if url_time > 180:
            time_out = True
            log.logger.error("接口等待时间过久，没反应")
            break
        res = json.loads(r.text)
        if res['code'] == 200 and res['message'] == "SUCCESS":
            audioRecordId = res['data']['input']['audioRecordId']
            log.logger.info("接口/sjtu/api/test/buildInputAndSent访问成功")
            break
    if time_out :
        return None
    else:
        with io.open(input_json, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(json.loads(r.text), ensure_ascii=False))
            f.close()
    return audioRecordId

def output_url(audioRecordId, result_path):
    """
    :param audioRecordId: 记录id
    :param result_path: output.json存放目录
    :return: output 的json格式
    """
    log.logger.info("*******************************************************")
    log.logger.info("正在访问接口/sjtu/api/test/caseResultLisener，请稍等")
    url_time = 0
    # url1 = 'http://10.50.12.9:9001/sjtu/api/test/caseResultLisener'
    url = 'http://10.50.12.46:9001/sjtu/api/test/testResult'
    data = {}
    data['audioRecordId'] = audioRecordId
    log.logger.info("output中的接口输入;")
    log.logger.info (json.dumps(data, ensure_ascii=False))
    sys.stdout.flush()
    while True:
        r1 = requests.post(url, data=data)
        res1 = json.loads(r1.text)
        sys.stdout.flush()
        time.sleep(5)
        url_time += 5
        if url_time > 600:
            break
        if res1['code'] == 200:
            # log.logger.info("output中的接口输出:")
            # log.logger.info(json.dumps(res1, ensure_ascii=False))
            output = res1
            log.logger.info("接口/sjtu/api/test/caseResultLisener访问成功")
            break
    if url_time > 600:
        output = None

    else:
        with open(result_path, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(res1, ensure_ascii=False))
            f.close()
    return output




if __name__ ==  "__main__":
    input_config = {'config': '''{"sid":"SH00PD_963201101","description":"内资新设",audioRecordId:""}'''}
    images_path = "D:/08八卦/02test/test_sources_labels/SH00PD_963201101/样例/1"
    files = eachFile(images_path)
    #log.logger.info(files)
    autoRecordId = input_url(input_config, images_path)
    log.logger.info(autoRecordId)
    # autoRecordId = '1115500478881333248'
    # output_url(autoRecordId, os.path.join(os.path.dirname(__file__),'output.json'))

