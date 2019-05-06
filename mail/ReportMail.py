# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 15:50
# @Author  : Yang
# @Email   : 494056012@qq.com
# @File    : ReportMail.py
# @Software: PyCharm
import smtplib, time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import os
import sys
# path1 = os.path.join(sys.path[1],'config.py')
# sys.path.append(path1)

#import config
# path = os.path.join(os.path.join(config.report_path,'reportlist'),str(time.strftime("%Y%m%d", time.localtime())+'Report.html'))

def testReport_mail(path, runner):
    # 第三方 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "sjtu_notice@seassoon.com"  # 用户名
    mail_pass = "Sjtu123!"  # 口令

    sender = 'sjtu_notice@seassoon.com'
    receivers = ['wudan@seassoon.com', 'duanjiangang@seassoon.com','chenchao@seassoon.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # receivers = ['songyang@seassoon.com']

    # 发送邮件主题
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    subject = '自动化测试结果_' + t

    # 读取html文件内容
    mail_html = r"""
  <!DOCTYPE html>
<!-- saved from url=(0024)http://10.50.12.46:5002/ -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title>浦东审批自动化测试每日报告概况</title>
<link href="./自动化测试报告总览_files/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<h1 align="left" ,style="font-family: Microsoft YaHei;text-align: center">浦东审批自动化测试每日报告概况 </h1>
<br>
<font align="left" size= '4'>开始时间: %(start_time)s</font>
</br>
<br>
<font align="left" size = '4'>运行时间:%(run_time)s </font>
</br>
<br>
<font align="left" size = '4'>状态: %(status)s</font>
</br>
<br>
<a href= "http://10.50.12.46:5009/index.html",align="center",style="font-family: Microsoft YaHei">自动化测试报告汇总</a>
</br>
<br>
<a href= "http://10.50.12.46:5009/%(report_name)s",align="center",style="font-family: Microsoft YaHei">详情页面查看http://10.50.12.46:5009</a>
</br>
</body>"""

       # .format(time.strftime('%Y%m%d',time.localtime(time.time()))+'Report.html')
    status = [u'总计事项 %s' % (runner.case_num)]
    status.append(u'通过事项 %s' % runner.case_pass)
    status.append(u'失败事项 %s' % runner.case_fail)
    status.append(u'错误事项 %s' % runner.case_err)
    status.append(u'可忽略 %s' % runner.case_ignore)
    status.append(u'不可忽略 %s' % runner.case_unignore)
    if status:
        status = ' '.join(status)
    else:
        status = 'none'
    mail_body = mail_html % dict(
        start_time = str(runner.startTime),
        run_time = str(runner.stopTime - runner.startTime),
        status = status ,
        report_name = time.strftime('%Y%m%d',time.localtime(time.time()))+'Report.html'
    )

    # 组装邮件内容和标题，中文需参数‘utf-8’，单字节字符不需要
    message = MIMEMultipart()
    att3 = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
    att3["Content-Type"] = 'application/octet-stream'
    att3["Content-Disposition"] = 'attachment; filename= {}'.format(os.path.split(path)[-1])
    # print(os.path.split(path)[-1])
    message.attach(att3)

    mail_inside = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header("浦东人工智能辅助审批事项测试报告", 'utf-8')

    message['To'] = Header(';'.join(receivers), 'utf-8')
    message.attach(mail_inside)



    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
    except:
        print("邮件发送失败！")
    else:
        print("邮件发送成功！")
    finally:
        smtpObj.quit()


if __name__ == "__main__":
    path = os.path.join('D:\\08 八卦\\02 test\\bagua_auto_test\\test_cases', 'res_report_1.html')

    testReport_mail(path)
