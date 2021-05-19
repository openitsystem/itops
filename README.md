# 系统介绍

基于Python + Django的AD管理系统，系统主要提供以下功能:

* 丰富的API接口，便于内部系统的集成
* 在线邮件流查询
* 常规AD、Exchange操作的WEB化，更友好的交互体验
* 2FA认证登陆，角色权限分层。增强系统安全性的同时，提升HelpDesk同学解决问题的效率
* 丰富的报表功能和批量操作功能
* 详细的日志功能

详细功能可参见[基于web的AD、Exchange管理平台](https://www.opscaff.com/2019/04/28/%E5%9F%BA%E4%BA%8Ead%E3%80%81exchange%E7%9A%84%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0/)



# ITOPS安装部署文档

* 系统要求
* centos安装python3
* 安装程序
* 运行程序
* 系统配置并开始使用


## Docker部署
```powershell
# 容器镜像下载
docker pull openitsystem/itops:1.0.1

# 启动容器
docker run -d -p 8080:8080 openitsystem/itops:1.0.1
```

## 1.系统要求：

### 基础环境
* Active directory 2008R2
* DC 2008R2
* PowerShell 版本 4.0 以上
* Exchange 2010 & 2016
* 在Exchange服务器上执行以下操作
  * 在链接邮箱服务器右键已管理员身份运行powershell，输入以下命令，按Y确认：
  ```powershell
  Set-ExecutionPolicy RemoteSigned
  ```
  * 在链接邮箱服务器依次点击：开始——管理工具——Internet Information Services (IIS)管理器，进入iis管理器。依次展开：计算机名——网站——Default Web Site——PowerShell，双击“身份验证”，右键启用“基本身份验证”

### 部署服务器要求
* centos:7.x
* python:3.5.x
* MySQL 5.7

> 基于提供的虚拟机部署，直接跳至5.系统配置

## 2.centos安装python3
### 2.1.建议停用防火墙

```
systemctl  stop firewalld  (停用防火墙）
```

### 2.2.安装依赖关系：(更新下yum)

```
yum update

yum groupinstall 'Development Tools' -y

yum install zlib-devel openssl-devel ncurses-devel bzip2-devel \

expat-devel gdbm-devel readline-devel sqlite-devel -y
```
### 2.3.下载安装包
* [在python官网下载](https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz)

### 2.4.解压文件并安装python

```
tar -xf Python-3.5.2.tgz
```
> 解压之后生成Python-3.5.2目录，并进入

```
cd Python-3.5.2
```
> 开始安装，使用编译的方法进行安装,在python的目录中有一个README文件，他介绍了如何安装python。 但是我们要指定这个安装目录

```
mkdir /usr/python35

./configure --prefix=/usr/python35

make

make install
```
### 2.5.检查python环境

```
[root ~]# /usr/python35/bin/python3.5
Python 3.5.2 (default, May 27 2020, 16:58:18) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
[root ~]# 

```
> /usr/python35/bin/python3.5 -m pip list #查看已安装的包

```
[root ~]# /usr/python35/bin/python3.5 -m pip list
Package                 Version   
----------------------- ----------
appdirs                 1.4.3     
APScheduler             2.1.2     
asn1crypto              0.24.0    
cached-property         1.3.0     
cffi                    1.12.3    
...
[root ~]#
```
## 3.安装系统
### 3.1.把运行程序拷贝到指定目录
> 将itops文件夹拷贝到 /usr/local/ 下（注意不要改文件名）

> 拷贝完成后路径为 /usr/local/itops/

> 使用 xftp 5 或其他方式拷贝均可

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_one.png)

### 3.2.安装项目运行所必须的包
> 更新pip

```
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple --upgrade pip
```

> 进入代码目录

```
cd /usr/local/itops/
```
> 确认目录中有requirements.txt文件（此文件中放了所必须的包名）

```
ls
```
> 安装所有的包

```
/usr/python35/bin/python3.5 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple -r requirements.txt
```

> 安装完成后,再次检查

```
/usr/python35/bin/python3.5 -m pip list
```

### 3.3.赋予权限

```
cd /usr/local/ \
    && chmod 777 itops/

cd /usr/local/itops/ \
    && chmod 777 db.sqlite3 \
    && chmod 777 upload/

cd /usr/local/itops/dbinfo/ \
    && chmod 777 config.ini

```
## 4.启动服务
### 4.1.启动uwsgi服务
> 运行下列命令启动平台服务

```
/usr/python35/bin/uwsgi --http-socket 0.0.0.0:8080 --chdir /usr/local/itops/ --plugin python --wsgi-file /usr/local/itops/itops/wsgi.py --master --static-map /static=/usr/local/itops/static/ --static-map /static=/usr/local/itops/frontend/dist/static/ --static-map /static=/usr/python35/lib/python3.5/site-packages/rest_framework/static/ --processes 2 --threads 2 --static-gzip-dir=/usr/local/itops/frontend/
```
> 关闭uwsgi

```
pkill -9 uwsgi 
```
## 5.系统配置
### 5.1.基于提供的vm虚拟机部署
#### 5.1.1.启动uwsgi服务
> 虚拟机默认自启动了uwsgi服务，即可以直接通过http://IP:8080 访问系统,并且每次重启centos系统都会自动启动uwsgi ,你也可以通过以下命令对uwsgi进行管理

```
supervisord 客户端管理命令
supervisorctl status           #状态
supervisorctl stop uwsgi         #停止 uwsgi
supervisorctl start uwsgi        #启动 uwsgi
supervisorctl restart uwsgi       #重启 uwsgi
```
#### 5.1.2.账号密码

```
centos账户:root 
centos密码：QW*963.（注意最后有个点)

mysql账户：root  
mysql密码：tcQW*963@2019  
mysql端口：3306  
mysql数据库名称：ops
mysqip:centos服务器IP

平台登录路径 http://IP:8080
平台配置管理员账户：adminportal
平台配置管理员密码：tcQW*963@2019
```
#### 5.1.3.平台配置

```
初次登录请使用 http://Ip:8080访问，并使用内置配置管理账号登录，进行系统配置
平台配置管理员账户：adminportal
平台配置管理员密码：tcQW*963@2019
```

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_two.png)

#### 5.1.4.更改平台配置管理员账户密码
请牢记此密码，以后每次更新配置，都需用adminportal账号进入

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_three.png)

#### 5.1.5.数据库配置

```
虚拟机中已内置安装了mysql 无需单独安装
mysql账户：root  
mysql密码：tcQW*963@2019  
mysql端口：3306  
mysql数据库名称：ops
mysqip:虚拟机IP
```
配置完成请点击提交

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_four.png)
#### 5.1.6.LDAP配置

```
AD服务器地址：除RODC外的任意DCIP
域名：AD域名
账号密码：具有管理员权限的账号，账号格式 contoso\administrator（账号前去除域名后缀如:.com、.cn等）
默认查找起始：建议根目录 示例 dc=contoso,dc=com
是否开启加密连接：强烈建议启用加密链接，否则无法进行密码相关操作
```

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_six.png)

配置完成请点击提交

#### 5.1.7.EXChange 配置

```
EXChange服务器地址：具有powershell4.0 的CAS服务器
账号密码：具有exchange管理员的账号  账号格式:exadmin 注意此处不要用domain\account的形式，直接填写账号
域名：AD域名
```

![](https://www.opscaff.com/wp-content/uploads/2019/05/c51406fd166189c4f07166ac5c8fdab2.png)

配置完成请点击提交
#### 5.1.8.账号权限配置
配置此项前，请先点击页面左下角重载配置，然后再用adminportal登录后进行配置

```
组名定义：AD组属性sAMAccountName中的名称。

当赋予AD中某个组具有相应的权限后,即该组中的成员就具有相同的权限。

注意：登录判断是通过组嵌套实现，即其余3个组必须是 具有登录权限的组的成员,否则无法登录。但是我们在您点击提交时,会自动将其余3个组加入到登录组的成员。但需要您保证组嵌套的合规性。例如 通用组不能是全局组的成员。如嵌套失败，请您手动修改组属性合规并手动嵌套
```
> 各组权限定义：

具有登录权限的 | 具有修改密码的组 | 具有修改栏位的组 | 具有操作权限的组
---|---|---|---
IT记录管理（增删改查 | IT记录管理（增删改查） | IT记录管理（增删改查）| 所有权限
搜索，查看用户,计算机等属性 | 搜索，查看用户,计算机等属性 | 搜索，查看用户,计算机等属性 | 所有权限
邮件流查询 | 邮件流查询 | 邮件流查询 |  所有权限
查看文档、新建文档、可以修改删除自己的文档 | 查看文档、新建文档、可以修改删除自己的文档 | 查看文档、新建文档、可以修改删除自己的文档 | 所有权限
API文档查看 | API文档查看 | API文档查看 | 所有权限
--- | 修改用户密码 | 可以修改账户，组织选项卡中的： 电话号码，主页， 移动电话号码，传真，寻呼机， IP电话字段 | 所有权限

> 组名请填写组的sAMAccountName中的名称

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_eight.png)

配置完成请点击提交

#### 5.1.9.开始使用
当您所有属性配置完成并确认无误后，请点击 配置已全部完成,点击返回使用

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_nine.png)

此时可以使用域账号登录并管理了

![](https://www.opscaff.com/wp-content/uploads/2019/05/picture_nine.png)

**每次更新MySQL数据库配置、LDAP 配置，必须重载配置才能生效（重载配置时，服务暂时不可用）**
### 5.2.基于源代码自行部署

```
平台管理员账户：adminportal

平台管理员密码：tcQW*963@2019
```
#### 5.2.1
> 启动服务的方式请参照 请参照 4.1.启动uwsgi服务  启动和关闭程序,并且每次重启centos程序都不会自动运行,需手动运行命令（或者自行使用supervisor实现5.1.启动uwsgi服务的方式）

#### 5.2.2
> 参照**5.1.3.平台配置** 开始至 **5.1.9.开始使用** ，并将 **5.1.5.数据库配置** 中的信息换成自己的数据库信息


# 欢迎贡献代码或提issue



