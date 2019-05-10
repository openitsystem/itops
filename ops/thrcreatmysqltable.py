# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 10:41
# @Author  :
import threading

from dbinfo.models import dbinfo
from dbinfo.views import insert_log_table_name


class ThrCreatMysqlTable(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        conn = dbinfo()
        if conn:
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'django_session'"
                conncur.execute(connsql)
                django_session = conncur.fetchone()
                conn.commit()
                if not django_session:
                    conncur = conn.cursor()
                    connsql = '''DROP TABLE IF EXISTS `django_session`;
                    CREATE TABLE `django_session` (
                      `session_key` varchar(40) NOT NULL,
                      `session_data` longtext NOT NULL,
                      `expire_date` datetime(6) NOT NULL,
                      PRIMARY KEY (`session_key`),
                      KEY `django_session_expire_date_a5c62663` (`expire_date`) USING BTREE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'django_session', '创建django_session表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'apiusers_profile'"
                conncur.execute(connsql)
                apiusers_profile = conncur.fetchone()
                conn.commit()
                if not apiusers_profile:
                    conncur = conn.cursor()
                    connsql = '''
                    DROP TABLE IF EXISTS `apiusers_profile`;
                    CREATE TABLE `apiusers_profile` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `password` varchar(128) NOT NULL,
                      `last_login` datetime(6) DEFAULT NULL,
                      `is_superuser` tinyint(1) NOT NULL,
                      `username` varchar(150) NOT NULL,
                      `first_name` varchar(30) NOT NULL,
                      `last_name` varchar(30) NOT NULL,
                      `email` varchar(254) NOT NULL,
                      `is_staff` tinyint(1) NOT NULL,
                      `is_active` tinyint(1) NOT NULL,
                      `date_joined` datetime(6) NOT NULL,
                      `name` varchar(50) DEFAULT NULL,
                      `department` varchar(255) DEFAULT NULL,
                      `description` varchar(255) DEFAULT NULL,
                      PRIMARY KEY (`id`),
                      UNIQUE KEY `username` (`username`) USING BTREE
                    ) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'apiusers_profile', '创建apiusers_profile表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'apiusers_apinamepermissions'"
                conncur.execute(connsql)
                apiusers_apinamepermissions = conncur.fetchone()
                conn.commit()
                if not apiusers_apinamepermissions:
                    conncur = conn.cursor()
                    connsql = '''
                    DROP TABLE IF EXISTS `apiusers_apinamepermissions`;
                    CREATE TABLE `apiusers_apinamepermissions` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `apiname` varchar(50) NOT NULL,
                      `username_id` int(11) NOT NULL,
                      PRIMARY KEY (`id`),
                      KEY `apiusers_permissions_username_id_10b067f1_fk_apiusers_profile_id` (`username_id`) USING BTREE,
                      CONSTRAINT `apiusers_apinamepermissions_ibfk_2` FOREIGN KEY (`username_id`) REFERENCES `apiusers_profile` (`id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'apiusers_apinamepermissions', '创建apiusers_apinamepermissions表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'apiusers_attributeslevel'"
                conncur.execute(connsql)
                apiusers_attributeslevel = conncur.fetchone()
                conn.commit()
                if not apiusers_attributeslevel:
                    conncur = conn.cursor()
                    connsql = '''
                    DROP TABLE IF EXISTS `apiusers_attributeslevel`;
                    CREATE TABLE `apiusers_attributeslevel` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `apiname` varchar(255) NOT NULL,
                      `attributes` mediumtext,
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
                    conncur = conn.cursor()
                    connsql = '''
                                INSERT INTO `apiusers_attributeslevel` VALUES ('1', 'EXSetMailbox1', "['CN','Sn','Givename','Initials','displayName','Description', 'physicalDeliveryOfficeName','telephoneNumber','Mail', 'wWWHomePage','C','St','L','streetAddress','postOfficeBox','postalCode','homePhone','Pager','mobile','FacsimileTelephoneNumber','ipPhone','Info','Title','Department','Company','ProhibitSendQuota','ProhibitSendReceiveQuota','RecipientLimits','UseDatabaseQuotaDefaults','IssueWarningQuota','RulesQuota','ArchiveName','ArchiveQuota','ArchiveWarningQuota','Office']");
                                INSERT INTO `apiusers_attributeslevel` VALUES ('2', 'EXSetMailbox2', "['CN','Sn','Givename','Initials','displayName','Description', 'physicalDeliveryOfficeName','telephoneNumber','Mail', 'wWWHomePage','C','St','L','streetAddress','postOfficeBox','postalCode','homePhone','Pager','mobile','FacsimileTelephoneNumber','ipPhone','Info','Title','Department','Company','ProhibitSendQuota','ProhibitSendReceiveQuota','RecipientLimits','UseDatabaseQuotaDefaults','IssueWarningQuota','RulesQuota','ArchiveName','ArchiveQuota','ArchiveWarningQuota','Office','accountExpires','memberOf','sAMAccountName','member','memberOf','managedBy','Alias','EmailAddressPolicyenabled','PrimarySmtpAddress']");
                                INSERT INTO `apiusers_attributeslevel` VALUES ('3', 'Ldap3SetAccountLevel1', "['CN','Sn','Givename','Initials','displayName','Description', 'physicalDeliveryOfficeName','telephoneNumber','Mail', 'wWWHomePage','C','St','L','streetAddress','postOfficeBox','postalCode','homePhone','Pager','mobile','FacsimileTelephoneNumber','ipPhone','Info','Title','Department','Company','ProhibitSendQuota','ProhibitSendReceiveQuota','RecipientLimits','UseDatabaseQuotaDefaults','IssueWarningQuota','RulesQuota','ArchiveName','ArchiveQuota','ArchiveWarningQuota','Office']");
                                INSERT INTO `apiusers_attributeslevel` VALUES ('4', 'Ldap3SetAccountLevel2', "['CN','Sn','Givename','Initials','displayName','Description', 'physicalDeliveryOfficeName','telephoneNumber','Mail', 'wWWHomePage','C','St','L','streetAddress','postOfficeBox','postalCode','homePhone','Pager','mobile','FacsimileTelephoneNumber','ipPhone','Info','Title','Department','Company','ProhibitSendQuota','ProhibitSendReceiveQuota','RecipientLimits','UseDatabaseQuotaDefaults','IssueWarningQuota','RulesQuota','ArchiveName','ArchiveQuota','ArchiveWarningQuota','Office','accountExpires','memberOf','sAMAccountName','member','memberOf','managedBy','Alias','EmailAddressPolicyenabled','PrimarySmtpAddress']");

                                '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'apiusers_attributeslevel', '创建apiusers_attributeslevel表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'LDAPAttributes'"
                conncur.execute(connsql)
                LDAPAttributes = conncur.fetchone()
                conn.commit()
                if not LDAPAttributes:
                    conncur = conn.cursor()
                    connsql = '''
                    DROP TABLE IF EXISTS `LDAPAttributes`;
                    CREATE TABLE `LDAPAttributes` (
                      `id` int(255) NOT NULL AUTO_INCREMENT,
                      `Name` varchar(255) DEFAULT NULL,
                      `LDAPName` varchar(255) DEFAULT NULL,
                      `CNName` varchar(255) DEFAULT NULL,
                      `type` varchar(255) DEFAULT NULL,
                      `typeName` varchar(255) DEFAULT NULL,
                      `NameUrl` varchar(255) DEFAULT NULL,
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

                    '''
                    conncur.execute(connsql)
                    conn.commit()
                    conncur = conn.cursor()
                    connsql = '''
                                INSERT INTO `LDAPAttributes` VALUES ('1', 'First Name', 'givenName', '名字', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('2', 'Middle Name / Initials', 'initials', '中间名首字母缩写', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('3', 'Last Name', 'sn', '姓氏', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('4', 'Logon Name', 'userPrincipalName', '登录名', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('5', 'Logon Name (Pre Windows 2000)', 'sAMAccountName', '登录名(Windows 2000以前版本)', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('6', 'Display Name', 'displayName', '显示名称', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('7', 'Full  Name', 'cn', '全名', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('8', 'Description', 'description', '描述', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('9', 'Office', 'physicalDeliveryOfficeName', '办公室', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('10', 'Telephone Number', 'telephoneNumber', '电话号码', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('11', 'Email', 'mail', '电子邮件', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('12', 'Web Page', 'wWWHomePage', '网页', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('14', 'Street', 'streetAddress', '街道', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('15', 'PO Box', 'postOfficeBox', '邮政信箱', 'list', '多值字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('16', 'City', 'l', '市/县(地址选项卡)', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('17', 'State/Province', 'st', '省/自治区', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('18', 'Zip/Postal Code', 'postalCode', '邮政编码', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('19', 'Country ', 'co', '国家 - 例如 中国', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('20', 'Country 2', 'c', '国家2数字代码 - 例如。我们  CN', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('21', 'Country code', 'countryCode', '国家代码-eg。对于中国国家代码是156', 'int', '整数', null);
                                INSERT INTO `LDAPAttributes` VALUES ('22', 'Add to Groups', 'memberOf', '隶属于(成员)', 'list', '多值字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('24', 'Account Expires (use same date format as server)', 'accountExpires', '账户过期', 'datetime', '大整数', null);
                                INSERT INTO `LDAPAttributes` VALUES ('25', 'User Account Control ', 'userAccountControl', '用户帐户控制', 'int', '整数', null);
                                INSERT INTO `LDAPAttributes` VALUES ('26', 'User Photo ', 'thumbnailPhoto', '用户照片', 'str', '八进制字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('27', 'Profile Path', 'profilePath', '配置文件路径(配置文件选项卡)', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('28', 'Login Script', 'scriptPath', '登录脚本', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('29', 'Home Folder', 'homeDirectory', '本地路径', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('30', 'Home', 'homePhone', '家庭电话', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('31', 'Pager', 'pager', '寻呼机', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('32', 'Mobile', 'mobile', '移动电话', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('33', 'Fax', 'facsimileTelephoneNumber', '传真', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('34', 'IP Phone', 'ipPhone', 'IP电话', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('35', 'Notes', 'info', '注释(电话选项卡)', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('36', 'Title', 'title', '职务', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('37', 'Department', 'department', '部门', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('38', 'Company', 'company', '公司', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('39', 'Manager', 'manager', '管理者', 'str', '字符串', null);
                                INSERT INTO `LDAPAttributes` VALUES ('40', 'msDS-UserPasswordExpiryTimeComputed', 'msDSUserPasswordExpiryTimeComputed', '密码过期时间', 'datetime', '大整数', null);
                                INSERT INTO `LDAPAttributes` VALUES ('41', 'whenCreated', 'whenCreated', '创建时间(R)', 'datetime', '时间属性：所有时间均为格林威治标准时间(GMT)', null);
                                INSERT INTO `LDAPAttributes` VALUES ('42', 'whenChanged', 'whenChanged', '修改时间(M)', 'datetime', '时间属性：所有时间均为格林威治标准时间(GMT)', null);
                                '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'LDAPAttributes', '创建LDAPAttributes表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'usertoken'"
                conncur.execute(connsql)
                usertoken = conncur.fetchone()
                conn.commit()
                if not usertoken:
                    conncur = conn.cursor()
                    connsql = '''DROP TABLE IF EXISTS `usertoken`;
                        CREATE TABLE `usertoken` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `username` varchar(255) DEFAULT NULL,
                        `token` varchar(255) DEFAULT NULL,
                        `date` datetime DEFAULT NULL,
                        PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'usertoken', '创建usertoken表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'Mess'"
                conncur.execute(connsql)
                Mess = conncur.fetchone()
                conn.commit()
                if not Mess:
                    conncur = conn.cursor()
                    connsql = '''DROP TABLE IF EXISTS `Mess`;
                        CREATE TABLE `Mess` (
                          `id` int(11) NOT NULL AUTO_INCREMENT,
                          `title` varchar(255) DEFAULT NULL,
                          `tab` varchar(255) DEFAULT NULL,
                          `message` longtext,
                          `user` varchar(255) DEFAULT NULL,
                          `date` datetime DEFAULT NULL,
                          PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'Mess', '创建Mess表', str(e))
            try:
                conncur = conn.cursor()
                connsql = "show tables like 'messgerro'"
                conncur.execute(connsql)
                messgerro = conncur.fetchone()
                conn.commit()
                if not messgerro:
                    conncur = conn.cursor()
                    connsql = '''DROP TABLE IF EXISTS `messgerro`;
                            CREATE TABLE `messgerro` (
                              `id` int(11) NOT NULL AUTO_INCREMENT,
                              `title` varchar(255) DEFAULT NULL,
                              `userper` varchar(255) DEFAULT NULL,
                              `accfet` varchar(255) DEFAULT NULL,
                              `datetime` varchar(255) DEFAULT NULL,
                              `tips` varchar(255) DEFAULT NULL,
                              `marke` longtext,
                              `creatuser` varchar(255) DEFAULT NULL,
                              `creatime` datetime DEFAULT NULL,
                              PRIMARY KEY (`id`)
                            ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
                    '''
                    conncur.execute(connsql)
                    conn.commit()
            except Exception as e:
                insert_log_table_name('log', '127.0.0.1', 'ThrCreatMysqlTable', 'adminportal', 'False', 'messgerro', '创建messgerro表', str(e))
        return 1



def creatmysqltable():
    '''
    创建mysql数据库的一些表格
    1.异步
    2.连接数据库
    3.判断表格是否存在
    4.不存在则新建
    :return:
    '''
    send_email = ThrCreatMysqlTable()
    send_email.start()

