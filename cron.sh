#!/bin/sh

cd /home/testing/bagua_auto_test

nohup /root/anaconda3/bin/python run_all_cases.py 2>&1 &
