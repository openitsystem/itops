# -*- coding: utf-8 -*-
# @Time    : 2018/12/21 10:31
# @Author  :
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import pymysql
import ast
import json

from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from ldap3 import Connection, Server

from dbinfo.Profile import writeprofile, readprofile
from dbinfo.encrypt_decode import encrypt_and_decode


# 测试
def dbinfotest(host,username,password,port,database):
    try:
        conn = pymysql.connect(host=host, port=int(port), user=username, password=password,
                               database=database,
                               charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        if not cur:
            return False
        else:
            return True
    except Exception as e:
        return False
#邮件发送测试
def mailtest(inputadd,myysqlusername,myysqlpassword,inputserver,inputtestmail):
    # 第三方 SMTP 服务
    mail_host = inputserver # 设置服务器
    mail_user = myysqlusername # 用户名
    mail_pass = myysqlpassword  # 口令

    sender = inputadd
    receivers =  inputtestmail # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText('平台测试邮件内容', 'plain', 'utf-8')
    subject = '测试邮件主题'
    message['Subject'] = Header(subject, 'utf-8')
    message['To'] = Header(inputtestmail, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False

# ladp测试
def ldaptest(adip, aduser, adpassword,sele):
    try:
        if sele==1:
            ussl=True
        else:
            ussl=False
        conn = Connection(Server(host=adip, use_ssl=ussl), user=aduser,
                          password=adpassword, auto_bind=True)
        if conn:
            return True
        else:
            return False
    except Exception as e:
        return False

#创建首页数据表
def crearindexmessagedb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql ='''CREATE TABLE `indexmessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `allusercountvalue` varchar(255) DEFAULT '0' comment '所有用户数量',
  `alldisableusercountvalue` varchar(255) DEFAULT '0' comment '禁用用户数量',
  `allexpiredpasswordusercountvalue` varchar(255) DEFAULT '0' comment '密码已过期用户数量',
  `alllockusercountvalue` varchar(255) DEFAULT '0' comment '锁定用户数量',
  `nologoinusercountvalue` varchar(255) DEFAULT '0' comment '账号30天之内未登录的账号数量',
  `allgroupcountvalue` varchar(255) DEFAULT '0' comment '所有群组数量',
  `allgrouptalkgroupcountvalue` varchar(255) DEFAULT '0' comment '通讯组数量',
  `allgroupsavegroupcpuntvalue` varchar(255) DEFAULT '0' comment '安全组数量',
  `allgroupnomembercountvalue` varchar(255) DEFAULT '0' comment '没有成员的组数量',
  `allgrouphasmailcountvalue` varchar(255) DEFAULT '0' comment '启用邮箱的组数量',
  `allcomputercountvalue` varchar(255) DEFAULT '0' comment '所有计算机数量',
  `allcomputernologoincountvalue` varchar(255) DEFAULT '0' comment '超过30天没有登录的计算机数量',
  `allcomputernodisablecpuntvalue` varchar(255) DEFAULT '0' comment '启用的计算机数量',
  `allcomputerdisablecountvalue` varchar(255) DEFAULT '0' comment '禁用的计算机数量',
  `allexchangeusercountvalue` varchar(255) DEFAULT '0' comment '所有启用邮箱的用户数量',
  `allnoexchangeusercountvalue` varchar(255) DEFAULT '0' comment '所有未启用邮箱的用户数量',
  `allexchangehasarchivecpuntvalue` varchar(255) DEFAULT '0' comment '已启用归档的账户数量',
  `allexchangenodizhicountvalue` varchar(255) DEFAULT '0' comment '不显示在exchange地址簿的用户数量',
  `allexchangenoarchivecountvalue` varchar(255) DEFAULT '0' comment '禁用归档的账户数量',
  `datetime` datetime DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4'''
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


def dbinfo():
    try:
        host = readprofile('mysql', 'host')
        username = readprofile('mysql', 'username')
        Port = readprofile('mysql', 'Port')
        database = readprofile('mysql', 'database')
        password = encrypt_and_decode().decrypted_text(readprofile('mysql', 'password'))
        #测试
        conn = pymysql.connect(host=host, port=int(Port), user=username, password=password,
                               database=database,
                               charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        if cur:
            return conn
        else:
            return False
    except Exception as e:
        return False

#验证ldap表是否存在
def selectldapdb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "show tables like 'ldap3_configtion'"
        conncur.execute(connsql)
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
#创建ldap表
def crearldapdb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql ='''CREATE TABLE `ldap3_configtion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) DEFAULT NULL,
  `server` varchar(255) DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `search_base` varchar(255) DEFAULT NULL,
  `use_ssl` tinyint(255) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8'''
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#创建y邮箱表
def crearmaildb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql ='''CREATE TABLE `sendmailsite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailcount` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `mailserver` varchar(255) DEFAULT NULL,
  `mailaddress` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4'''
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False


#验证ldap表是否存在
def selectiisex():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "show tables like 'exiisconfig'"
        conncur.execute(connsql)
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)


#创建操作表
def crearperdb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql ='''CREATE TABLE `UserPer` (
  `id` int(11) NOT NULL DEFAULT '0',
  `logongroup` varchar(255) DEFAULT NULL,
  `changepwdgroup` varchar(255) DEFAULT NULL,
  `fieldgroup` varchar(255) DEFAULT NULL,
  `operagroup` varchar(255) DEFAULT NULL,
  `monitor` varchar(255) DEFAULT '0' COMMENT '是否开启监控',
  `zabbixurl` varchar(255) DEFAULT NULL,
  `zabbixuser` varchar(255) DEFAULT NULL,
  `zabbixpassword` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8'''
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def searchsendmail():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from sendmailsite limit1"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#验证邮箱表是否存在
def selectmaildb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "show tables like 'sendmailsite'"
        conncur.execute(connsql)
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)


#验证操作表是否存在
def selectperdb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "show tables like 'UserPer'"
        conncur.execute(connsql)
        histroycounts = conncur.fetchone()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)

def insert_sendmail(mailcount,password, mailserver,mailaddress):
    createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from sendmailsite"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE sendmailsite SET mailcount=%s,password=%s, mailserver=%s,mailaddress=%s,datetime=%s WHERE id =%s"
            conncur.execute(connsql, (mailcount,password, mailserver,mailaddress,createtime,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO sendmailsite (mailcount,password, mailserver,mailaddress,datetime) VALUES (%s,%s,%s,%s,%s) "
            conncur.execute(connsql, (mailcount, password, mailserver, mailaddress, createtime))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_userper(logongroup,changepwdgroup, fieldgroup,operagroup):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from UserPer"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE UserPer SET logongroup=%s,changepwdgroup=%s, fieldgroup=%s,operagroup=%s WHERE id =%s"
            conncur.execute(connsql, (logongroup,changepwdgroup, fieldgroup,operagroup,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO UserPer (logongroup,changepwdgroup, fieldgroup,operagroup) VALUES (%s,%s,%s,%s) "
            conncur.execute(connsql, (logongroup,changepwdgroup, fieldgroup,operagroup))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_userper_monitor(monitor):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from UserPer"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE UserPer SET monitor = %s WHERE id =%s"
            conncur.execute(connsql, (monitor,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO UserPer (monitor) VALUES (%s) "
            conncur.execute(connsql, (monitor))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

def insert_userper_zabbix(monitor,zabbixurl,zabbixuser,zabbixpassword):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from UserPer"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id = histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE UserPer SET monitor = %s,zabbixurl=%s,zabbixuser=%s,zabbixpassword=%s WHERE id =%s"
            conncur.execute(connsql, (monitor,zabbixurl,zabbixuser,zabbixpassword, id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO UserPer (monitor,zabbixurl,zabbixuser,zabbixpassword) VALUES (%s) "
            conncur.execute(connsql, (monitor,zabbixurl,zabbixuser,zabbixpassword))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

#ldap写入
def insert_ldapmessage(domian,adip,aduser,adpassword,adserchbase,sele):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "select * from ldap3_configtion"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE ldap3_configtion SET domain=%s,server=%s, user=%s,password=%s,search_base=%s ,use_ssl=%s WHERE id =%s"
            conncur.execute(connsql, (domian,adip,aduser,adpassword,adserchbase,sele,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO ldap3_configtion (domain,server, user,password,search_base,use_ssl) VALUES (%s,%s,%s,%s,%s,%s) "
            conncur.execute(connsql, (domian,adip,aduser,adpassword,adserchbase,sele))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False



#创建操作表
def creariisdb():
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql ='''CREATE TABLE `exiisconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iisserver` varchar(255) DEFAULT NULL,
  `iisport` varchar(255) DEFAULT NULL,
  `exserver` varchar(255) DEFAULT NULL,
  `exuser` varchar(255) DEFAULT NULL,
  `expassword` varchar(255) DEFAULT NULL,
  `exdomain` varchar(255) DEFAULT NULL,
  `skey` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;'''
        conncur.execute(connsql)
        histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

# #iis信息写入
# def insert_iisexpmessage(iisip,iisport):
#     conn = dbinfo()
#     try:
#         conncur = conn.cursor()
#         connsql = "select * from exiisconfig"
#         conncur.execute(connsql, ())
#         histroycounts = conncur.fetchone()
#         if histroycounts:
#             id =histroycounts['id']
#             conncur = conn.cursor()
#             connsql = "UPDATE exiisconfig SET iisserver=%s,iisport=%s WHERE id =%s"
#             conncur.execute(connsql, (iisip,iisport,id))
#             histroycounts = conncur.fetchall()
#         else:
#             conncur = conn.cursor()
#             connsql = "INSERT INTO exiisconfig (iisserver,iisport) VALUES (%s,%s) "
#             conncur.execute(connsql, (iisip,iisport))
#             histroycounts = conncur.fetchall()
#         conn.commit()
#         conn.close()
#         return histroycounts
#     except Exception as e:
#         print(e)
#         return False


#exchange信息写入
def insert_expmessage(exinputip,exinputaccount,password,exinputdomain):
    conn = dbinfo()
    try:
        conncur = conn.cursor()
        connsql = "show tables like 'exiisconfig'"
        conncur.execute(connsql, ())
        exiisconfig = conncur.fetchone()
        conn.commit()
        if not exiisconfig:
            conncur = conn.cursor()
            connsql = '''DROP TABLE IF EXISTS `exiisconfig`;
                        CREATE TABLE `exiisconfig` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `exserver` varchar(255) DEFAULT NULL,
                        `exuser` varchar(255) DEFAULT NULL,
                        `expassword` varchar(255) DEFAULT NULL,
                        `exdomain` varchar(255) DEFAULT NULL,
                        PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
                                '''
            conncur.execute(connsql)
            conn.commit()
        conncur = conn.cursor()
        connsql = "select * from exiisconfig"
        conncur.execute(connsql, ())
        histroycounts = conncur.fetchone()
        if histroycounts:
            id =histroycounts['id']
            conncur = conn.cursor()
            connsql = "UPDATE exiisconfig SET exserver=%s,exuser=%s,expassword=%s,exdomain=%s WHERE id =%s"
            conncur.execute(connsql, (exinputip,exinputaccount,password,exinputdomain,id))
            histroycounts = conncur.fetchall()
        else:
            conncur = conn.cursor()
            connsql = "INSERT INTO exiisconfig (exserver,exuser,expassword,exdomain) VALUES (%s,%s,%s,%s) "
            conncur.execute(connsql, (exinputip,exinputaccount,password,exinputdomain))
            histroycounts = conncur.fetchall()
        conn.commit()
        conn.close()
        return histroycounts
    except Exception as e:
        print(e)
        return False

# #iisskey
# def insert_iisekey(skeyvalue):
#     conn = dbinfo()
#     try:
#         conncur = conn.cursor()
#         connsql = "select * from exiisconfig"
#         conncur.execute(connsql, ())
#         histroycounts = conncur.fetchone()
#         if histroycounts:
#             id =histroycounts['id']
#             conncur = conn.cursor()
#             connsql = "UPDATE exiisconfig SET skey=%s WHERE id =%s"
#             conncur.execute(connsql, (skeyvalue,id))
#             histroycounts = conncur.fetchall()
#         else:
#             conncur = conn.cursor()
#             connsql = "INSERT INTO exiisconfig (skey) VALUES (%s) "
#             conncur.execute(connsql, (skeyvalue))
#             histroycounts = conncur.fetchall()
#         conn.commit()
#         conn.close()
#         return histroycounts
#     except Exception as e:
#         print(e)
#         return False

def mysqllinktest(request):
    post = request.POST
    host = post.get("host")
    username = post.get("username")
    password = post.get("password")
    port = post.get("port")
    database = post.get("database")
    try:
        if dbinfotest(host,username,password,port,database):
            # dir_now = os.path.dirname(os.path.abspath("settings.py"))
            writeprofile("mysql", "host", host)
            writeprofile("mysql", "username", username)
            writeprofile("mysql", "password", encrypt_and_decode().encrypted_text(password))
            writeprofile("mysql", "port", port)
            writeprofile("mysql", "database", database)
            result = {'isSuccess': True, 'message': '修改mysql配置成功'}
        else:
            result = {'isSuccess': False, 'message': '修改mysql配置失败'}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    except Exception as e:
        result = {'isSuccess': False, 'message': '修改mysql配置失败：'+str(e)}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response

