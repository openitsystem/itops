$(document).ready(function () {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue'
    });
});
//设置垂直滚动条
$(document).ready(function () {
    var height = $(document.body).height() - 100;
    $('.chat-room,.chat-contacts').slimScroll({
        color: '#eee',
        size: '5px',
        height: height,
        alwaysVisible: true
    });
});

$.ajax({
    url: "/show_domain/",
    type: 'POST',
    dataType: 'json',
    async: false,
    success: function (data) {
        zNodes = data["message"];
    }
});//生成OU初始数

var setting = {
    async: {
        enable: true, //表示异步加载生效
        url: "/show_ou_for_dn/",// 异步加载时访问的页面
        autoParam: ["distinguishedName", "id"], // 异步加载时自动提交的父节点属性的参数
        //otherParam:["paths"], //ajax请求时提交的参数
        type: 'post',
        dataType: 'json'
    },
    view: {
        expandSpeed: "",//zTree 节点展开、折叠时的动画速度
        //addHoverDom: addHoverDom,//用于当鼠标移动到节点上时，显示用户自定义控件
        //removeHoverDom: removeHoverDom, //用于当鼠标移出节点时，隐藏用户自定义控件
        selectedMulti: false ////设置是否允许同时选中多个节点。
    },
    edit: {
        drag: {
            autoExpandTrigger: true, //拖拽时父节点自动展开是否触发 onExpand 事件回调函数
            prev: false, //拖拽到目标节点时，设置是否允许移动到目标节点前面的操作
            inner: true,//拖拽到目标节点时，设置是否允许成为目标节点的子节点
            next: false, //拖拽到目标节点时，设置是否允许移动到目标节点后面的操作
        },
        enable: true,//设置 zTree 是否处于编辑状态
        showRemoveBtn: false,//设置是否显示删除按钮
        showRenameBtn: false,//设置是否显示编辑名称按钮
    },
    data: {
        simpleData: {
            enable: true
        }
    },//设置数据格式为id

    check: {
        enable: false,//设置 zTree 的节点上是否显示 checkbox / radio
        chkStyle: "checkbox",
        chkboxType: {"Y": "s", "N": "s"},//只影响子节点
    },
    callback: { // 回调函数
        onClick: zTreeOnClick, // 单击鼠标事件
        onRightClick: OnRightClick,//捕获 zTree 上鼠标右键点击之后的事件回调函数
        beforeDrag: beforeDrag,//用于捕获节点被拖拽之前的事件回调函数，并且根据返回值确定是否允许开启拖拽操作
        beforeDrop: beforeDrop//用于捕获节点拖拽操作结束之前的事件回调函数，并且根据返回值确定是否允许此拖拽操作
    },
};
//点击事件
function zTreeOnClick() {
    var zTree = $.fn.zTree.getZTreeObj("treeDemo"), //zTree = Object {setting: Object} 根据 treeId 获取 zTree 对象的方法
        nodes = zTree.getSelectedNodes(), // nodes = [Object] 获取zTree当前被选中的节点数据集合
        treeNode = nodes[0];  // treeNode = Object {pid: 3, path: "OU=,OU=IT
    dataTreeReset(treeNode.distinguishedName)
}

var getOffset = {
    top: function (obj) {
        return obj.offsetTop + (obj.offsetParent ? arguments.callee(obj.offsetParent) : 0)
    },
    left: function (obj) {
        return obj.offsetLeft + (obj.offsetParent ? arguments.callee(obj.offsetParent) : 0)
    }
};

//拖拽事件
function beforeDrag(treeId, treeNodes) {
    for (var i = 0, l = treeNodes.length; i < l; i++) {
        if (treeNodes[i].drag === false) {
            return false;
        }
        if ([zNodes.name, "Builtin", "Computers", "ForeignSecurityPrincipals", "LostAndFound", "System", "Users", "Domain Controllers", "Infrastructure"].indexOf(treeNodes[i].name) > -1) {
            return false;
        }
    }
    return true;
}

function beforeDrop(treeId, treeNodes, targetNode, moveType) {
    swal({
        title: 'Active Directory 域服务',
        text: "在Active Directory 域服务中移动对象可能导致现有系统无法按设计的方式工作。例如，移动组织单位(OU)可能影响组策略应用到OU内账户的方式。 您确定要移动此对象吗?",
        type: "warning",
        showCancelButton: true,
        confirmButtonText: '是(Y)',//使用此选项可更改“确认”按钮上的文本。
        cancelButtonText: '否(N)',//使用此选项可更改“取消”按钮上的文本。
        closeOnConfirm: false,
        showLoaderOnConfirm: false,
    }, function () {
        if (targetNode.drop == false) {
            return false;
        } else {
            if (targetNode) {
                var nodesDn = [];
                for (var i = 0, l = treeNodes.length; i < l; i++) {
                    nodesDn.push(treeNodes[i].distinguishedName)
                }
                var targetDn = targetNode.distinguishedName;
                $.ajax({
                    url: "/moveDnsToOu/",
                    type: 'POST',
                    dataType: 'json',
                    data: {'dns': nodesDn, 'new_superior': targetDn},
                    success: function (data) {
                        if (data['isSuccess']) {
                            if (data['count'] == 0) {
                                swal({
                                    title: "全部移动成功",
                                    text: '',
                                    type: "success",
                                    showConfirmButton: "true",
                                    confirmButtonText: "好的",
                                    animation: "slide-from-top",
                                    showCancelButton: false,
                                    closeOnConfirm: true
                                }, function () {
                                    resetDrop(treeId, treeNodes[0].distinguishedName, targetDn);
                                    return true;
                                })
                            } else {
                                resetDrop(treeId, treeNodes[0].distinguishedName, targetDn);
                                swal.close();
                                $("#dorpTable tbody").html("");
                                for (var i = 0, l = data['message'].length; i < l; i++) {
                                    $("#dorpTable tbody").append("<tr><td>" + data['message'][i]['cn'] + "</td><td>" + data['message'][i]['moveresult'] + "</td></tr>")
                                }
                                $('#dorpErrors').modal({
                                    keyboard: true,
                                    backdrop: false
                                });
                                return true;
                            }
                        }
                        else {
                            resetDrop(treeId, treeNodes[0].distinguishedName, targetDn);
                            sweetAlert("errors", data['message'], "error");
                            return true;
                        }
                    }
                });
            } else {
                return false;
            }
        }

    })
    resetDrop(treeId, treeNodes[0].distinguishedName, targetNode.distinguishedName);
    return false;
}

function resetDrop(treeId, treeNodesdn, targetNodedn) {
    if (treeId == 'treeDemo') {
        var path_dn = targetNodedn.split(',');
        path_dn.splice(0, 1, path_dn[0]);
        var path_dn2 = path_dn.join(',');
        treeReset('treeDemo', path_dn2);
        var path_distinguishedName = treeNodesdn.split(',');
        path_distinguishedName.splice(0, 1, path_distinguishedName[0])
        var path_distinguishedName2 = path_distinguishedName.join(',');
        treeReset('dataTree', path_distinguishedName2);
    } else {
        var path_dn = targetNodedn.split(',');
        path_dn.splice(0, 1, path_dn[0]);
        var path_dn2 = path_dn.join(',');
        treeReset('dataTree', path_dn2);
        var path_distinguishedName = treeNodesdn.split(',');
        path_distinguishedName.splice(0, 1, path_distinguishedName[0])
        var path_distinguishedName2 = path_distinguishedName.join(',');
        treeReset('treeDemo', path_distinguishedName2);
    }

}
// 在ztree treeDemo上的右击事件
function OnRightClick(event, treeId, treeNode) {
    if (!treeNode && event.target.tagName.toLowerCase() != "button" && $(event.target).parents("a").length == 0) {
        zTree.cancelSelectedNode();
    } else if (treeNode && !treeNode.noR) {
        zTree.selectNode(treeNode);
        showRMenu(treeNode, event.clientX, event.clientY);
    }
}

function showRMenu(treeNode, x, y) {
    var oMenu = document.getElementById("rightMenu");
    var aUl = oMenu.getElementsByTagName("ul");
    var aLi = oMenu.getElementsByTagName("li");
    var showTimer = hideTimer = null;
    var i = 0;
    var maxWidth = maxHeight = 0;
    var aDoc = [document.documentElement.offsetWidth, document.documentElement.offsetHeight];
    $("#rightMenu").show();
    $("#treeDemo_rename").show();
    $("#treeDemo_add").show();
    $("#treeDemo_move").show();
    $("#treeDemo_del").show();
    $("#treeDemo_exportList").show();
    if (["Builtin", "Computers", "ForeignSecurityPrincipals", "LostAndFound", "System", "Users", "Domain Controllers"].indexOf(treeNode.name) > -1) {
        $("#treeDemo_rename").hide();
        $("#treeDemo_move").hide();
        $("#treeDemo_del").hide();
    }
    if (treeNode.objectClass.toString() != ["top", "organizationalUnit"].toString()) {
        $("#treeDemo_add").hide();
        $("#treeDemo_exportList").hide();
    }
    if (zNodes.name==treeNode.name){
        $("#treeDemo_add").show();
        $("#treeDemo_exportList").show();
        $("#treeDemo_rename").hide();
        $("#treeDemo_move").hide();
        $("#treeDemo_del").hide();
    }
    for (i = 0; i < aLi.length; i++) {
        //为含有子菜单的li加上箭头
        aLi[i].getElementsByTagName("ul")[0] && (aLi[i].className = "sub");

        //鼠标移入
        aLi[i].onmouseover = function () {
            var oThis = this;
            var oUl = oThis.getElementsByTagName("ul");
            //鼠标移入样式
            oThis.className += " active";

            //显示子菜单
            if (oUl[0]) {
                clearTimeout(hideTimer);
                showTimer = setTimeout(function () {
                    for (i = 0; i < oThis.parentNode.children.length; i++) {
                        oThis.parentNode.children[i].getElementsByTagName("ul")[0] &&
                        (oThis.parentNode.children[i].getElementsByTagName("ul")[0].style.display = "none");
                    }
                    oUl[0].style.display = "block";
                    oUl[0].style.top = oThis.offsetTop + "px";
                    oUl[0].style.left = oThis.offsetWidth + "px";
                    setWidth(oUl[0]);

                    //最大显示范围
                    maxWidth = aDoc[0] - oUl[0].offsetWidth;
                    maxHeight = aDoc[1] - oUl[0].offsetHeight;

                    //防止溢出
                    maxWidth < getOffset.left(oUl[0]) && (oUl[0].style.left = -oUl[0].clientWidth + "px");
                    maxHeight < getOffset.top(oUl[0]) && (oUl[0].style.top = -oUl[0].clientHeight + oThis.offsetTop + oThis.clientHeight + "px")
                }, 300);
            }
        };

        //鼠标移出
        aLi[i].onmouseout = function () {
            var oThis = this;
            var oUl = oThis.getElementsByTagName("ul");
            //鼠标移出样式
            oThis.className = oThis.className.replace(/\s?active/, "");

            clearTimeout(showTimer);
            hideTimer = setTimeout(function () {
                for (i = 0; i < oThis.parentNode.children.length; i++) {
                    oThis.parentNode.children[i].getElementsByTagName("ul")[0] &&
                    (oThis.parentNode.children[i].getElementsByTagName("ul")[0].style.display = "none");
                }
            }, 300);
        };
    }
    //自定义右键菜单
    document.oncontextmenu = function (event) {
        var event = event || window.event;
        oMenu.style.display = "block";
        oMenu.style.top = event.clientY + "px";
        oMenu.style.left = event.clientX + "px";
        setWidth(aUl[0]);

        //最大显示范围
        maxWidth = aDoc[0] - oMenu.offsetWidth;
        maxHeight = aDoc[1] - oMenu.offsetHeight;

        //防止菜单溢出
        oMenu.offsetTop > maxHeight && (oMenu.style.top = maxHeight + "px");
        oMenu.offsetLeft > maxWidth && (oMenu.style.left = maxWidth + "px");
        return false;
    };

    //取li中最大的宽度, 并赋给同级所有li
    function setWidth(obj) {
        maxWidth = 80;
        for (i = 0; i < obj.children.length; i++) {
            var oLi = obj.children[i];
            var iWidth = oLi.clientWidth - parseInt(oLi.currentStyle ? oLi.currentStyle["paddingLeft"] : getComputedStyle(oLi, null)["paddingLeft"]) * 2
            if (iWidth > maxWidth) maxWidth = iWidth;
        }
        for (i = 0; i < obj.children.length; i++) obj.children[i].style.width = maxWidth + "px";
    }

    y += document.body.scrollTop;
    x += document.body.scrollLeft;
    if ($(window).width() > 990) {
        x = x - $("#menu").width();
    }
    $("#rightMenu").css({"top": y + "px", "left": x + "px", "visibility": "visible"});
    $("body").bind("mousedown", onBodyMouseDown);
}
function hideRMenu() {
    if ($("#rightMenu")) $("#rightMenu").css({"visibility": "hidden"});
    $("body").unbind("mousedown", onBodyMouseDown);
}
function onBodyMouseDown(event) {
    if (!(event.target.id == "rMenu" || $(event.target).parents("#rMenu").length > 0)) {
        $("#rightMenu").css({"visibility": "hidden"});
    }
}

var zTree, rMenu, zNodes;
$(document).ready(function () {
    $.fn.zTree.init($("#treeDemo"), setting, zNodes);//初始化zTree
    zTree = $.fn.zTree.getZTreeObj("treeDemo");
    rMenu = $("#rightMenu");
    var nodes = zTree.getNodes();
    if (nodes.length > 0) {
        for (var i = 0; i < nodes.length; i++) {
            zTree.expandNode(nodes[i], true, false, false);//默认展开第一级节点
        }
    }

});

//重命名的方法
function renameObject(get_select_node, treename) {
    var distinguishedName = get_select_node.distinguishedName;
    var ou = get_select_node.ou; //姓名(U)
    var cn = get_select_node.cn; //姓名(U)
    var sn = get_select_node.sn;
    var givenName = get_select_node.givenName;
    var displayName = get_select_node.displayName;
    var userPrincipalName = get_select_node.userPrincipalName;
    var sAMAccountName = get_select_node.sAMAccountName;
    var objectClass = get_select_node.objectClass;
    switch (objectClass.toString()) {
        case ["top", "container"].toString():
            document.getElementById("ou_treename").value = treename;
            document.getElementById("ou_name").value = cn;
            document.getElementById("ou_distinguishedName").value = distinguishedName;
            document.getElementById("ou_objectClass").value = objectClass;
            $('#rename_ou').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case ["top", "organizationalUnit"].toString():
            document.getElementById("ou_treename").value = treename;
            document.getElementById("ou_name").value = ou[0];
            document.getElementById("ou_distinguishedName").value = distinguishedName;
            document.getElementById("ou_objectClass").value = objectClass;
            $('#rename_ou').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case ["top", "group"].toString():
            document.getElementById("group_treename").value = treename;
            document.getElementById("group_name").value = cn;
            document.getElementById("group_distinguishedName").value = distinguishedName;
            document.getElementById("group_objectClass").value = objectClass;
            document.getElementById("group_sAMAccountName").value = sAMAccountName;
            $('#rename_group').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case ["top", "person", "organizationalPerson", "contact"].toString():
            document.getElementById("contact_treename").value = treename;
            document.getElementById("contact_name").value = cn;
            document.getElementById("contact_distinguishedName").value = distinguishedName;
            document.getElementById("contact_objectClass").value = objectClass;
            document.getElementById("contact_sn").value = sn;
            document.getElementById("contact_givenName").value = givenName;
            document.getElementById("contact_displayName").value = displayName;
            $('#rename_contact').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case ["top", "person", "organizationalPerson", "user"].toString():
            document.getElementById("user_treename").value = treename;
            document.getElementById("user_name").value = cn;
            document.getElementById("user_distinguishedName").value = distinguishedName;
            document.getElementById("user_objectClass").value = objectClass;
            document.getElementById("user_sn").value = sn;
            document.getElementById("user_givenName").value = givenName;
            document.getElementById("user_displayName").value = displayName;
            document.getElementById("user_sAMAccountName1").value = zNodes.domain;
            document.getElementById("user_sAMAccountName2").value = sAMAccountName;
            if (userPrincipalName.length > 0) {
                userPrincipalName = userPrincipalName.split('@')
                document.getElementById("user_userPrincipalName1").value = userPrincipalName[0];
                document.getElementById("user_userPrincipalName2").value = "@" + userPrincipalName[1];
            } else {
                document.getElementById("user_userPrincipalName2").value = zNodes.upn;
            }

            $('#rename_user').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        default:
            swal('这个对象暂时无法重命名');
    }
}
//执行重命名的方法
function rename_object(object, obj) {
    var distinguishedName, ou, cn, sn, givenName, displayName, userPrincipalName, sAMAccountName, objectClass, treename, new_name;
    switch (object) {
        case 'ou':
            cn = document.getElementById("ou_name").value;
            ou = document.getElementById("ou_name").value;
            distinguishedName = document.getElementById("ou_distinguishedName").value;
            objectClass = document.getElementById("ou_objectClass").value;
            treename = document.getElementById("ou_treename").value;
            if (["top", "organizationalUnit"].toString() == objectClass.toString()) {
                new_name = "OU=" + cn;
            } else {
                new_name = "CN=" + cn;
            }
            break;
        case 'group':
            cn = document.getElementById("group_name").value;
            distinguishedName = document.getElementById("group_distinguishedName").value;
            objectClass = document.getElementById("group_objectClass").value;
            sAMAccountName = document.getElementById("group_sAMAccountName").value;
            treename = document.getElementById("group_treename").value;
            new_name = "CN=" + cn;
            break;
        case 'user':
            cn = document.getElementById("user_name").value;
            distinguishedName = document.getElementById("user_distinguishedName").value;
            objectClass = document.getElementById("user_objectClass").value;
            sn = document.getElementById("user_sn").value;
            givenName = document.getElementById("user_givenName").value;
            displayName = document.getElementById("user_displayName").value;
            sAMAccountName = document.getElementById("user_sAMAccountName2").value;
            userPrincipalName = document.getElementById("user_userPrincipalName1").value + document.getElementById("user_userPrincipalName2").value;
            treename = document.getElementById("user_treename").value;
            new_name = "CN=" + cn;
            break;
        case 'contact':
            cn = document.getElementById("contact_name").value;
            distinguishedName = document.getElementById("contact_distinguishedName").value;
            objectClass = document.getElementById("contact_objectClass").value;
            sn = document.getElementById("contact_sn").value;
            givenName = document.getElementById("contact_givenName").value;
            displayName = document.getElementById("contact_displayName").value;
            treename = document.getElementById("contact_treename").value;
            new_name = "CN=" + cn;
            break;
    }
    if (distinguishedName.length > 0 && cn.length > 0) {
        $(obj).attr('disabled', true);
        $.ajax({
            url: "/setRenameObject/",
            type: 'POST',
            dataType: 'json',
            data: {
                'distinguishedName': distinguishedName, 'cn': cn, 'sn': sn, 'givenName': givenName, 'displayName': displayName, 'userPrincipalName': userPrincipalName
                , 'sAMAccountName': sAMAccountName, 'objectClass': objectClass
            },
            success: function (data) {
                if (data['isSuccess']) {
                    $(obj).attr('disabled', false);
                    swal({
                        title: "",
                        text: data['message'],
                        type: "success",
                        showConfirmButton: "true",
                        confirmButtonText: "好的",
                        animation: "slide-from-top"
                    });
                    $("#rename_user").modal("hide");
                    $("#rename_contact").modal("hide");
                    $("#rename_group").modal("hide");
                    $("#rename_ou").modal("hide");
                    var path_dn = (distinguishedName).split(',')
                    path_dn.splice(0, 1, new_name)
                    var path_dn2 = path_dn.join(',')
                    treeReset(treename, path_dn2)

                } else {
                    $(obj).attr('disabled', false);
                    swal("修改失败：" + data['message']);
                    treeReset(treename, distinguishedName)
                }
            }
        });

    } else {
        swal("不能为空！")
    }
}
//添加对象的方法
function addObject(get_select_node, objectclass) {
    var distinguishedName = get_select_node.distinguishedName;
    switch (objectclass) {
        case "user":
            document.getElementById('add_user_distinguishedName').value = distinguishedName;
            document.getElementById('add_user_userPrincipalName2').value = zNodes.upn;
            document.getElementById('add_user_sAMAccountName1').value = zNodes.domain;
            document.getElementById('add_user_sn').value = '';
            document.getElementById('add_user_givenName').value = '';
            document.getElementById('add_user_cn').value = '';
            document.getElementById('add_user_userPrincipalName1').value = '';
            document.getElementById('add_user_sAMAccountName2').value = '';
            document.getElementById('add_user_password').value = '';
            document.getElementById('add_user_displayName').value = '';
            document.getElementById('add_user_description').value = '';
            $.ajax({
                url: "/getMailboxDatebase/",
                type: 'POST',
                dataType: 'json',
                async: true,
                success: function (data) {
                    if (data['isSuccess']) {
                        var $add_user_mail_db = $("#add_user_mail_db")
                        $add_user_mail_db.empty();
                        var message = data['message'];
                        for (var i = 0; i < message.length; i++) {
                            var $newOption = "<option value='" + message[i]['daname'] + "'>" + message[i]['daname'] + "</option>";
                            $add_user_mail_db.append($newOption);
                        }
                    }
                }
            });
            $('#add_user').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case "group":
            document.getElementById('add_group_distinguishedName').value = distinguishedName;
            document.getElementById('add_group_cn').value = '';
            document.getElementById('add_group_sAMAccountName').value = '';
            document.getElementById('add_group_displayName').value = '';
            document.getElementById('add_group_description').value = '';
            $('#add_group').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case "organizationalUnit":
            document.getElementById('add_organizationalUnit_distinguishedName').innerHTML = distinguishedName;
            document.getElementById('add_organizationalUnit_cn').value = '';
            $('#add_organizationalUnit').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case "contact":
            document.getElementById('add_contact_distinguishedName').value = distinguishedName;
            document.getElementById('add_contact_cn').value = '';
            document.getElementById('add_contact_displayName').value = '';
            document.getElementById('add_contact_description').value = '';
            document.getElementById('add_contact_name').value = '';
            document.getElementById('add_contact_smtpvalue').value = '';
            document.getElementById('add_contact_sn').value = '';
            document.getElementById('add_contact_givenName').value = '';
            $('#add_contact').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case "computer":
            document.getElementById('add_computer_distinguishedName').value = distinguishedName;
            document.getElementById('add_computer_cn').value = '';
            document.getElementById('add_computer_displayName').value = '';
            document.getElementById('add_computer_description').value = '';
            $('#add_computer').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        default:
            swal('无法在这个对象上新建');
    }
    ;
}

//执行添加对象的方法
$(document).ready(function () {
    $('#form_add_user').easyform();
    $('#form_add_control').easyform();
    $('#form_add_group').easyform();
    $('#form_add_computer').easyform();
});
function form_beforeSubmit() {
    showBg();
    return true
}
$(function () {
    var options_add_user = {
        beforeSubmit: form_beforeSubmit,
        dataType: "json",
        async: true,
        success: function (data) {
            if (data['isSuccess']) {
                $("#add_user").modal("hide");
                var distinguishedName = document.getElementById('add_user_distinguishedName').value;
                dataTreeReset(distinguishedName);
                closeBg();
                swal({
                    title: "",
                    text: data['message'],
                    type: "success",
                    showConfirmButton: "true",
                    confirmButtonText: "好的",
                    animation: "slide-from-top"
                });

            } else {
                closeBg();
                swal("新建失败：" + data['message']);

            }
        }
    }
    $("#form_add_user").ajaxForm(options_add_user);
    var options_add_control = {
        beforeSubmit: form_beforeSubmit,
        dataType: "json",
        async: true,
        success: function (data) {
            if (data['isSuccess']) {
                $("#add_contact").modal("hide");
                var distinguishedName = document.getElementById('add_contact_distinguishedName').value;
                dataTreeReset(distinguishedName);
                closeBg();
                swal({
                    title: "",
                    text: data['message'],
                    type: "success",
                    showConfirmButton: "true",
                    confirmButtonText: "好的",
                    animation: "slide-from-top"
                });

            } else {
                closeBg();
                swal("新建失败：" + data['message']);

            }
        }
    }
    $("#form_add_control").ajaxForm(options_add_control);
    var options_add_group = {
        beforeSubmit: form_beforeSubmit,
        dataType: "json",
        async: true,
        success: function (data) {
            if (data['isSuccess']) {
                $("#add_group").modal("hide");
                var distinguishedName = document.getElementById('add_group_distinguishedName').value;
                dataTreeReset(distinguishedName);
                closeBg();
                swal({
                    title: "",
                    text: data['message'],
                    type: "success",
                    showConfirmButton: "true",
                    confirmButtonText: "好的",
                    animation: "slide-from-top"
                });

            } else {
                closeBg();
                swal("新建失败：" + data['message']);

            }
        }
    }
    $("#form_add_group").ajaxForm(options_add_group);
    var options_add_computer = {
        beforeSubmit: form_beforeSubmit,
        dataType: "json",
        async: true,
        success: function (data) {
            if (data['isSuccess']) {
                $("#add_computer").modal("hide");
                var distinguishedName = document.getElementById('add_computer_distinguishedName').value;
                dataTreeReset(distinguishedName);
                closeBg();
                swal({
                    title: "",
                    text: data['message'],
                    type: "success",
                    showConfirmButton: "true",
                    confirmButtonText: "好的",
                    animation: "slide-from-top"
                });

            } else {
                closeBg();
                swal("新建失败：" + data['message']);

            }
        }
    }
    $("#form_add_computer").ajaxForm(options_add_computer);
});

//切换是否新建邮箱的方法
$(document).ready(function () {
    $("#add_user_mail").change(function () {
        var add_user_mail = $("#add_user_mail").val();
        if (add_user_mail == 'yes') {
            $("#modal_mail_db").css({"visibility": "visible"});
        } else {
            $("#modal_mail_db").css({"visibility": "hidden"});
        }
    });
    $("#add_contact_mail").change(function () {
        var add_contact_mail = $("#add_contact_mail").val();
        if (add_contact_mail == 'yes') {
            $(".contact_mail").css({"visibility": "visible"});
            document.getElementById("add_contact_name").disabled = "";
            document.getElementById("add_contact_smtpvalue").disabled = "";
        } else {
            $(".contact_mail").css({"visibility": "hidden"});
            document.getElementById("add_contact_name").disabled = "disabled";
            document.getElementById("add_contact_smtpvalue").disabled = "disabled";
        }
    });
});

function add_organizationalUnit(obj) {
    var distinguishedName = document.getElementById('add_organizationalUnit_distinguishedName').innerHTML;
    var cn = document.getElementById('add_organizationalUnit_cn').value;
    var checkbox = $("#add_organizationalUnit_checkbox").prop('checked')
    if (distinguishedName.length > 0 && cn.length > 0) {
        $(obj).attr('disabled', true);
        $.ajax({
            url: "/addorganizationalUnit/",
            type: 'POST',
            dataType: 'json',
            data: {'distinguishedName': distinguishedName, 'cn': cn, 'checkbox': checkbox},
            success: function (data) {
                if (data['isSuccess']) {
                    $("#add_organizationalUnit").modal("hide");
                    $(obj).attr('disabled', false);
                    dataTreeReset(distinguishedName);
                    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                    var nodes_path = treeObj.getNodesByParam("distinguishedName", distinguishedName, null);
                    if (nodes_path.length > 0) {
                        treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
                        treeObj.selectNode(nodes_path[0])
                    }
                    swal({
                        title: "",
                        text: data['message'],
                        type: "success",
                        showConfirmButton: "true",
                        confirmButtonText: "好的",
                        animation: "slide-from-top"
                    });
                } else {
                    $(obj).attr('disabled', false);
                    swal("新建失败：" + data['message']);
                }
            }
        });

    } else {
        swal("组名(A)不能为空!")
    }
}

//打开右键移动的方法模态框
function object_move_to_ou_modal(get_select_node, treename) {
    var distinguishedName = get_select_node.distinguishedName;
    var objectClass = get_select_node.objectClass;
    document.getElementById("object_move_distinguishedName").value = distinguishedName;
    document.getElementById("object_move_ztreename").value = treename;
    startztree()
    if (["top", "organizationalUnit"].toString() == objectClass.toString()) {

    }
    $('#object_move_to_ou_modal').modal({
        keyboard: true,
        backdrop: false
    });
}
//执行右键移动的方法
function setObjectMoveToOu(obj) {
    var ztreename = document.getElementById("object_move_ztreename").value;
    var object_move_distinguishedName = document.getElementById("object_move_distinguishedName").value;
    var ztreeou = $.fn.zTree.getZTreeObj("treemove");
    var get_select_node = ztreeou.getSelectedNodes()
    if (get_select_node.length > 0) {
        var object_move_ou_distinguishedName = get_select_node[0].distinguishedName;
        if (object_move_distinguishedName.length > 0) {
            $(obj).attr('disabled', true);
            $.ajax({
                url: "/setObjectMoveToOu/",
                type: 'POST',
                dataType: 'json',
                data: {'dn': object_move_distinguishedName, 'new_superior': object_move_ou_distinguishedName,},
                success: function (data) {
                    if (data['isSuccess']) {
                        $("#object_move_to_ou_modal").modal("hide");
                        var path_dn = (object_move_distinguishedName).split(',')
                        path_dn.splice(0, 1)
                        var path_dn2 = path_dn.join(',')
                        if (ztreename == 'treeDemo') {
                            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                            var nodes_path = treeObj.getNodesByParam("distinguishedName", path_dn2, null);
                            if (nodes_path.length > 0) {
                                treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
                                treeObj.selectNode(nodes_path[0])
                                dataTreeReset(path_dn2)
                            }
                        } else if (ztreename == 'dataTree') {
                            dataTreeReset(path_dn2)
                        }
                        $(obj).attr('disabled', false);
                        swal({
                            title: "",
                            text: data['message'],
                            type: "success",
                            showConfirmButton: "true",
                            confirmButtonText: "好的",
                            animation: "slide-from-top"
                        });
                    } else {
                        $(obj).attr('disabled', false);
                        swal("移动失败：" + data['message']);
                    }
                }
            });
        } else {
            swal('请选择需要移动的对象');
        }
    } else {
        swal('请选择需要移动到的OU');
    }


}

//点击右键方法合集
function rightMenuAll(treename, object, objectClass) {
    hideRMenu();//关闭弹框
    dataTreehideRMenu();
    var zTree_rename = $.fn.zTree.getZTreeObj(treename);
    var get_select_node = zTree_rename.getSelectedNodes()[0]
    if (get_select_node) {
        switch (object) {
            case 'objectMoveToOu'://移动
                object_move_to_ou_modal(get_select_node, treename); //移动
                break;
            case 'renameTreeNode'://重命名
                renameObject(get_select_node, treename);//重命名对象的方法
                break;
            case 'treeDemo_adds'://新建
                addObject(get_select_node, objectClass) //新建
                break;
            case 'treeDemoReset'://treeDemo刷新
                zTree_rename.reAsyncChildNodes(get_select_node, "refresh"); //刷新
                dataTreeReset(get_select_node.distinguishedName)
                break;
            case 'dataTreeReset'://dataTree刷新
                var distinguishedName = get_select_node.distinguishedName;
                var distinguishedNameList = distinguishedName.split(',');
                distinguishedNameList.splice(0, 1);
                var dn = distinguishedNameList.join()
                dataTreeReset(dn); //刷新第2颗树
                break;
            case 'objectAttribute'://属性
                objectAttribute(get_select_node, treename); //属性
                break;
            case 'del_object'://删除
                del_object(get_select_node, treename); //删除 打开模态框的方法
                break;
            case 'exportList'://导出列表(L)
                exportList(get_select_node, treename);
                break;
            case 'dataTree_enable_account'://启用账户
                setAccount(get_select_node, treename, '启用');
                break;
            case 'dataTree_disable_account'://禁用账户
                setAccount(get_select_node, treename, '禁用');
                break;
            case 'dataTree_reset_password'://重置密码
                showResetPassword(get_select_node.distinguishedName, get_select_node.sAMAccountName, get_select_node.lockoutTime);
                break;
            default:
                swal('这个对象暂时没有右键方法');

        }

    } else {
        swal("没有获取到数据");
    }
}
//刷新方法
function treeReset(treename, distinguishedName) {
    var zTree_rename = $.fn.zTree.getZTreeObj(treename);
    var distinguishedNameList = distinguishedName.split(',');
    distinguishedNameList.splice(0, 1);
    var dn = distinguishedNameList.join()
    if (treename == 'treeDemo') {
        var nodes = zTree_rename.getNodesByParam("distinguishedName", dn, null);
        if (nodes.length > 0) {
            zTree_rename.reAsyncChildNodes(nodes[0], "refresh"); //刷新
            var nodes_dn = zTree_rename.getNodesByParam("distinguishedName", distinguishedName, null);
            if (nodes_dn.length > 0) {
                zTree_rename.selectNode(nodes_dn[0])
            } else {
                zTree_rename.selectNode(nodes[0])
            }
        }

    } else if (treename == 'dataTree') {
        dataTreeReset(dn)
        var nodes_dn = zTree_rename.getNodesByParam("distinguishedName", distinguishedName, null);
        if (nodes_dn.length > 0) {
            zTree_rename.selectNode(nodes_dn[0])
        }
    }

}

//查看属性 跳转
function objectAttribute(get_select_node, treename) {
    var objectClass = get_select_node.objectClass;
    switch (objectClass.toString()) {
        case ["top", "container"].toString():
            openModle("/outhervalue/?disName=" + encodeURIComponent(get_select_node.distinguishedName));
            break;
        case ["top", "organizationalUnit"].toString():
            openModle("/outhervalue/?disName=" + encodeURIComponent(get_select_node.distinguishedName));
            break;
        case ["top", "group"].toString():
            openModle("/groupvalue/?disName=" + get_select_node.sAMAccountName);
            break;
        case ["top", "person", "organizationalPerson", "contact"].toString():
            openModle("/contactvalue/?disName=" + encodeURIComponent(get_select_node.distinguishedName));//modal-ifram 接新弹框contact
            break;
        case ["top", "person", "organizationalPerson", "user"].toString():
            openModle("/searchuser/?disName=" + get_select_node.sAMAccountName);//modal-ifram 接新弹框user
            break;
        case ["top", "person", "organizationalPerson", "user", "computer"].toString():
            openModle("/computervalue/?disName=" + get_select_node.sAMAccountName);//modal-ifram 接新弹框user
            break;
        default:
            openModle("/contactvalue/?disName=" + encodeURIComponent(get_select_node.distinguishedName));//modal-ifram 接新弹框contact
            break;
    }


}
//删除方法-打开模态框
function del_object(get_select_node, treename) {
    var objectClass = get_select_node.objectClass;
    var distinguishedName = get_select_node.distinguishedName;
    var objectName = (distinguishedName.split(',')[0]).split('=')[1]
    document.getElementById("del_distinguishedName").value = distinguishedName;
    document.getElementById("del_objectClass").value = objectClass;
    document.getElementById("del_treename").value = treename;
    switch (objectClass.toString()) {
        case ["top", "container"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 容器 吗?";
            break;
        case ["top", "organizationalUnit"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 组织单位 吗?";
            break;
        case ["top", "group"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 组 吗?";
            break;
        case ["top", "person", "organizationalPerson", "contact"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 联系人 吗?";
            break;
        case ["top", "person", "organizationalPerson", "user"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 用户 吗?";
            break;
        case ["top", "person", "organizationalPerson", "user", "computer"].toString():
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 计算机 吗?";
            break;
        default:
            document.getElementById('del_object_label').innerHTML = "您确定要删除名为“" + objectName + "”的 未知对象 吗?";
    }
    $('#del_object').modal({
        keyboard: true,
        backdrop: false
    });

}

//删除方法-执行删除，打开OU 的模态框
function delObject(obj) {
    var inspectObject_date;
    var distinguishedName = document.getElementById("del_distinguishedName").value;
    var objectClass = document.getElementById("del_objectClass").value;
    var treename = document.getElementById("del_treename").value;
    if (objectClass.toString() == ["top", "container"].toString() || objectClass.toString() == ["top", "organizationalUnit"].toString()) {
        $.ajax({
            url: "/inspectObject/",
            type: 'POST',
            dataType: 'json',
            async: false,
            data: {'dn': distinguishedName, 'search_scope': 'LEVEL'},
            success: function (data) {
                inspectObject_date = data
            }
        });
    } else {
        inspectObject_date = {'isSuccess': true, 'count': 0, 'message': '没有其他用户'};
    }
    if (inspectObject_date.count == 0) {
        if (distinguishedName.length > 0) {
            $(obj).attr('disabled', true);
            $.ajax({
                url: "/delObject/",
                type: 'POST',
                dataType: 'json',
                data: {'dn': distinguishedName,},
                success: function (data) {
                    if (data['isSuccess']) {
                        var path_dn = (distinguishedName).split(',')
                        path_dn.splice(0, 1)
                        var path_dn2 = path_dn.join(',')
                        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                        var nodes_path = treeObj.getNodesByParam("distinguishedName", path_dn2, null);
                        if (nodes_path.length > 0) {
                            treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
                            treeObj.selectNode(nodes_path[0])
                            dataTreeReset(path_dn2)
                        }
                        dataTreeReset(path_dn2)
                        $("#del_object").modal("hide");
                        swal({
                            title: "",
                            text: data['message'],
                            type: "success",
                            showConfirmButton: "true",
                            confirmButtonText: "好的",
                            animation: "slide-from-top"
                        });
                        $(obj).attr('disabled', false);
                    } else {
                        swal("删除失败：" + data['message']);
                        $("#del_object").modal("hide");
                        $(obj).attr('disabled', false);
                    }
                }
            });
        }
    }
    else {
        var objectName = (distinguishedName.split(',')[0]).split('=')[1];
        document.getElementById("del_ou_distinguishedName").value = distinguishedName;
        document.getElementById("del_ou_objectClass").value = objectClass;
        document.getElementById("del_ou_treename").value = treename;
        document.getElementById("del_ou_label").innerHTML = "对象" + objectName + "  包含其他账户或对象。您确定要删除  及其包含的所有对象吗?";
        $("#del_ou_checkbox").removeAttr("checked");
        $("#del_object").modal("hide");
        $('#del_ou').modal({
            keyboard: true,
            backdrop: false
        });
        document.getElementById("del_ou_div").style.display = "none"
        document.getElementById("del_ou_checkboxtext").value = '';
    }
}
$("#del_ou_checkbox").change(function () {
    var checkbox = $("#del_ou_checkbox").prop('checked');
    if (checkbox) {
        document.getElementById("del_ou_div").style.display = "block";
        document.getElementById("del_ou_checkboxtext").value = '';
    } else {
        document.getElementById("del_ou_div").style.display = "none";
        document.getElementById("del_ou_checkboxtext").value = '';
    }
});
// 删除OU 确认删除子树目录
function delOu(obj) {
    var distinguishedName = document.getElementById("del_ou_distinguishedName").value;
    var checkboxtext = document.getElementById("del_ou_checkboxtext").value;
    var checkbox = $("#del_ou_checkbox").prop('checked');
    if (distinguishedName.length > 0) {
        if (checkbox) {
            if (checkboxtext != '删除下面所有账户或对象') {
                swal("请填写：删除下面所有账户或对象");
                return false;
            } else {
                $(obj).attr("disabled", true);
                $.ajax({
                    url: "/delObject/",
                    type: 'POST',
                    dataType: 'json',
                    data: {'dn': distinguishedName, 'controls': checkbox, 'checkboxtext': checkboxtext},
                    success: function (data) {
                        if (data['isSuccess']) {
                            var path_dn = (distinguishedName).split(',')
                            path_dn.splice(0, 1)
                            var path_dn2 = path_dn.join(',')
                            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                            var nodes_path = treeObj.getNodesByParam("distinguishedName", path_dn2, null);
                            if (nodes_path.length > 0) {
                                treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
                                treeObj.selectNode(nodes_path[0])
                                dataTreeReset(path_dn2)
                            }
                            dataTreeReset(path_dn2)
                            $("#del_ou").modal("hide");
                            swal({
                                title: "",
                                text: data['message'],
                                type: "success",
                                showConfirmButton: "true",
                                confirmButtonText: "好的",
                                animation: "slide-from-top"
                            });
                            $(obj).attr("disabled", false);
                        } else {
                            swal("删除失败：" + data['message']);
                            $("#del_ou").modal("hide");
                            $(obj).attr("disabled", false);
                        }
                    }
                });
            }
        } else {
            $(obj).attr("disabled", true);
            $.ajax({
                url: "/delObject/",
                type: 'POST',
                dataType: 'json',
                data: {'dn': distinguishedName, 'controls': checkbox, 'checkboxtext': checkboxtext},
                success: function (data) {
                    if (data['isSuccess']) {
                        var path_dn = (distinguishedName).split(',')
                        path_dn.splice(0, 1)
                        var path_dn2 = path_dn.join(',')
                        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                        var nodes_path = treeObj.getNodesByParam("distinguishedName", path_dn2, null);
                        if (nodes_path.length > 0) {
                            treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
                            treeObj.selectNode(nodes_path[0])
                            dataTreeReset(path_dn2)
                        }
                        dataTreeReset(path_dn2)
                        $("#del_ou").modal("hide");
                        swal({
                            title: "",
                            text: data['message'],
                            type: "success",
                            showConfirmButton: "true",
                            confirmButtonText: "好的",
                            animation: "slide-from-top"
                        });
                        $(obj).attr("disabled", false);
                    } else {
                        swal("删除失败：" + data['message']);
                        $("#del_ou").modal("hide");
                        $(obj).attr("disabled", false);
                    }
                }
            });
        }
    } else {
        swal("删除失败：传入空值");
        $("#del_ou").modal("hide");
    }

}

//执行导出列表(L) 的方法或者打开模态框
function exportList(get_select_node, treename) {
    var objectClass = get_select_node.objectClass;
    var distinguishedName = get_select_node.distinguishedName;
    var sAMAccountName = get_select_node.sAMAccountName;
    switch (objectClass.toString()) {
        case ["top", "organizationalUnit"].toString():
            document.getElementById("export_list_distinguishedName").value = distinguishedName;
            document.getElementById("export_list_objectClass").value = objectClass;
            document.getElementById("export_list_treename").value = treename;
            $("#export_list_checkbox").removeAttr("checked");
            $('#export_list').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        case ["top", "group"].toString():
            post_url = '/groupexport/?filter=' + distinguishedName + '&samename=' + sAMAccountName;
            location.replace(post_url);
            break;
        case "domain":
            document.getElementById("export_list_distinguishedName").value = distinguishedName;
            document.getElementById("export_list_objectClass").value = objectClass;
            document.getElementById("export_list_treename").value = treename;
            $("#export_list_checkbox").removeAttr("checked");
            $('#export_list').modal({
                keyboard: true,
                backdrop: false
            });
            break;
        default:
            swal('这个对象暂时无法导出列表');
    }
}
// 执行OU导出列表(L)
function exportListObject() {
    var distinguishedName = document.getElementById("export_list_distinguishedName").value;
    var treename = document.getElementById("export_list_treename").value;
    var checkbox = $("#export_list_checkbox").prop('checked');
    if (distinguishedName.length > 0) {
        post_url = '/exportListToOU/?distinguishedName=' + distinguishedName + '&search_scope=' + checkbox;
        location.replace(post_url);
        $("#export_list").modal("hide");
    } else {
        swal("导出列表失败：传入空值");
        $("#export_list").modal("hide");
    }

}
//启用 禁用 账户
function setAccount(get_select_node, treename, type) {
    var userAccountControl = get_select_node.userAccountControl;
    var distinguishedName = get_select_node.distinguishedName;
    var sAMAccountName = get_select_node.sAMAccountName;
    if (type == '启用') {
        userAccountControl = parseInt(userAccountControl) - 2
    } else if (type == '禁用') {
        userAccountControl = parseInt(userAccountControl) + 2
    }
    if (distinguishedName.length > 0) {
        $.ajax({
            url: "/setObjectAttributes/",
            type: 'POST',
            dataType: 'json',
            data: {'distinguishedName': distinguishedName, 'attributesName': 'userAccountControl', 'attributesVaule': userAccountControl},
            success: function (data) {
                if (data['isSuccess']) {
                    var path_dn = (distinguishedName).split(',')
                    path_dn.splice(0, 1)
                    var path_dn2 = path_dn.join(',')
                    dataTreeReset(path_dn2)

                    swal({
                        title: "",
                        text: sAMAccountName + "对象,已" + type,
                        type: "success",
                        showConfirmButton: "true",
                        confirmButtonText: "好的",
                        animation: "slide-from-top"
                    });
                } else {
                    swal(sAMAccountName + "对象," + type + "失败");
                }
            }
        });
    } else {
        swal(sAMAccountName + "对象," + type + "失败：传入空值");
    }
}

//第2个ztree 树,做成treetable
//刷新第2颗树的方法
function dataTreeReset(dn) {
    showBg();
    $.ajax({
        url: "/show_object_for_dn/",
        type: 'POST',
        dataType: 'json',
        data: {'distinguishedName': dn,},
        success: function (data) {
            if (data['isSuccess']) {
                queryHandler(data['message']);
                closeBg();
            } else {
                queryHandler([]);
                closeBg();
                swal('获取数据错误');
            }
        }
    })
}

var newOpen = null;
$(function () {
    //初始化数据
    var data = []
    queryHandler(data);
});

var setting1 = {
    view: {
        showLine: false,
        showTitle: false,
        addDiyDom: addDiyDom,
        selectedMulti: true ////设置是否允许同时选中多个节点
    },
    edit: {
        drag: {
            autoExpandTrigger: true, //拖拽时父节点自动展开是否触发 onExpand 事件回调函数
            prev: false, //拖拽到目标节点时，设置是否允许移动到目标节点前面的操作
            inner: true,//拖拽到目标节点时，设置是否允许成为目标节点的子节点
            next: true, //拖拽到目标节点时，设置是否允许移动到目标节点后面的操作
        },
        enable: true,//设置 zTree 是否处于编辑状态
        showRemoveBtn: false,//设置是否显示删除按钮
        showRenameBtn: false,//设置是否显示编辑名称按钮
    },
    data: {
        simpleData: {
            enable: true,
        }
    }, check: {
        enable: false,//设置 zTree 的节点上是否显示 checkbox / radio
        chkStyle: "checkbox",
        chkboxType: {"Y": "s", "N": "s"},//只影响子节点
    },
    callback: { // 回调函数
        onClick: onClickHandle,
        onRightClick: dataTreeOnRightClick,//捕获 zTree 上鼠标右键点击之后的事件回调函数
        onDblClick: dataTreeonDblClick, // 双击击鼠标事件
        beforeDrag: beforeDrag,//用于捕获节点被拖拽之前的事件回调函数，并且根据返回值确定是否允许开启拖拽操作
        beforeDrop: beforeDrop//用于捕获节点拖拽操作结束之前的事件回调函数，并且根据返回值确定是否允许此拖拽操作
    },

};

//处理shift键多节点选择
function onClickHandle(event, treeId, treeNode) {
    var preClickedNode = window.preClickedNode;
    window.preClickedNode = treeNode;
    event = window.event || event;//兼容IE
    if (event.shiftKey && preClickedNode) {
        if ((!event.shiftKey && !event.srcEvent.shiftKey) || !preClickedNode) {//event.srcEvent.shiftKey解决firefox兼容性问题
            console.log("event ctrlKey error");
            return;// shift键
        }
        if (preClickedNode.getParentNode() != treeNode.getParentNode()) {  //是否同级
            preClickedNode = null;
            return;
        }
        var obj = jQuery.fn.zTree.getZTreeObj(treeId);
        obj.selectNode(preClickedNode, true); //选择
        var firstNode = obj.getNodeIndex(preClickedNode);
        var lastNode = obj.getNodeIndex(treeNode);
        var count = lastNode - firstNode;
        var nodeNew = preClickedNode;
        if (count > 0) {
            for (var i = 1; i < count; i++) {
                nodeNew = nodeNew.getNextNode();
                if (!nodeNew)break;//用于排除隐患
                obj.selectNode(nodeNew, true); //选择
                //obj.checkNode(nodeNew, true, true);//勾选
            }
        } else {
            for (var j = 1; j < (-count); j++) {
                nodeNew = nodeNew.getPreNode();
                if (!nodeNew)break;//用于排除隐患
                obj.selectNode(nodeNew, true); //选择
                //obj.checkNode(nodeNew, true, true);//勾选
            }
        }
    }

}


/**
 * 自定义DOM节点
 */
function selectNode(distinguishedName) {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getNodesByParam("distinguishedName", distinguishedName, null);
    if (nodes.length > 0) {
        treeObj.selectNode(nodes[0])
    }
    else {
        var path_dn = (distinguishedName).split(',')
        path_dn.splice(0, 1)
        var path_dn2 = path_dn.join(',')
        var nodes_path = treeObj.getNodesByParam("distinguishedName", path_dn2, null);
        if (nodes_path.length > 0) {
            treeObj.reAsyncChildNodes(nodes_path[0], "refresh"); //刷新
            treeObj.selectNode(nodes_path[0])
            // {#                    var treeObj1 = $.fn.zTree.getZTreeObj("treeDemo");#}
            // {#                    var dn_path = treeObj1.getNodesByParam("distinguishedName", distinguishedName, nodes_path[0]);#}
            // {#                    if (dn_path.length > 0) {#}
            // {#                        treeObj.selectNode(dn_path[0])#}
            // {#                    } else {#}
            // {#                        treeObj.selectNode(nodes_path[0])#}
            // {#                    }#}

            //var expandNode = treeObj.expandNode(nodes_path[0], true, false, true);
        }
    }
    return;
}

function dataTreeonDblClick(event, treeId, treeNode) {
    if (treeNode.types == '组织单位' || treeNode.types == '容器') {
        showBg();
        $.ajax({
            url: "/show_object_for_dn/",
            type: 'POST',
            dataType: 'json',
            data: {'distinguishedName': treeNode.distinguishedName,},
            success: function (data) {
                if (data['isSuccess']) {
                    queryHandler(data['message'])
                    closeBg();
                } else {
                    queryHandler([])
                    closeBg();
                }
            }

        })
        selectNode(treeNode.distinguishedName)
    }
    else if (treeNode.types == '用户') {
        openModle("/searchuser/?disName=" + treeNode.sAMAccountName);//modal-ifram 接新弹框user
    }
    else if ((treeNode.objectClass).toString() == ["top", "group"].toString()) {
        openModle("/groupvalue/?disName=" + treeNode.sAMAccountName);//modal-ifram
    }
    else if ((treeNode.objectClass).toString() == ["top", "person", "organizationalPerson", "user", "computer"].toString()) {
        openModle("/computervalue/?disName=" + treeNode.sAMAccountName);//modal-ifram 接新弹框user
    }
    else if ((treeNode.objectClass).toString() == ["top", "person", "organizationalPerson", "contact"].toString()) {
        openModle("/contactvalue/?disName=" + encodeURIComponent(treeNode.distinguishedName));//modal-ifram 接新弹框contact
    }

}

//dataTree右击事件
function dataTreeOnRightClick(event, treeId, treeNode) {
    dataTree.selectNode(treeNode);
    if (!treeNode && event.target.tagName.toLowerCase() != "button" && $(event.target).parents("a").length == 0) {
        dataTree.cancelSelectedNode();
    } else if (treeNode && !treeNode.noR) {
        dataTree.selectNode(treeNode);
        dataTreeshowRMenu(treeNode, event.clientX, event.clientY);
    }
}

function dataTreeshowRMenu(treeNode, x, y) {
    var oMenu = document.getElementById("rMenudataTree");
    var aUl = oMenu.getElementsByTagName("ul");
    var aLi = oMenu.getElementsByTagName("li");
    var showTimer = hideTimer = null;
    var i = 0;
    var maxWidth = maxHeight = 0;
    var aDoc = [document.documentElement.offsetWidth, document.documentElement.offsetHeight];
    $("#rMenudataTree").show();
    $("#dataTree_rename").show();
    $("#dataTree_add").show();
    $("#dataTree_del").show();
    $("#dataTree_move").show();

    $("#dataTree_exportList").show();

    $("#dataTree_reset_password").hide();
    $("#dataTree_enable_account").hide();//启用账户
    $("#dataTree_disable_account").hide();//禁用账户
    if ([zNodes.name, "Builtin", "Computers", "ForeignSecurityPrincipals", "LostAndFound", "System", "Users", "Domain Controllers"].indexOf(treeNode.name) > -1) {
        $("#dataTree_rename").hide();
        $("#dataTree_move").hide();
        $("#dataTree_del").hide();
    }
    if (treeNode.objectClass.toString() == ["top", "person", "organizationalPerson", "user", "computer"].toString()) {
        $("#dataTree_rename").hide();
        if (treeNode.Conte == "启用") {
            $("#dataTree_disable_account").show();
        } else if (treeNode.Conte == "禁用") {
            $("#dataTree_enable_account").show();
        }
    }
    if (treeNode.objectClass.toString() != ["top", "organizationalUnit"].toString()) {
        $("#dataTree_add").hide();
        $("#dataTree_exportList").hide();
    }
    if (treeNode.objectClass.toString() == ["top", "group"].toString()) {
        $("#dataTree_exportList").show();
    }
    if (treeNode.objectClass.toString() == ["top", "person", "organizationalPerson", "user"].toString()) {
        $("#dataTree_reset_password").show();
        if (treeNode.Conte == "启用") {
            $("#dataTree_disable_account").show();
        } else if (treeNode.Conte == "禁用") {
            $("#dataTree_enable_account").show();
        }

    }
    for (i = 0; i < aLi.length; i++) {
        //为含有子菜单的li加上箭头
        aLi[i].getElementsByTagName("ul")[0] && (aLi[i].className = "sub");

        //鼠标移入
        aLi[i].onmouseover = function () {
            var oThis = this;
            var oUl = oThis.getElementsByTagName("ul");
            //鼠标移入样式
            oThis.className += " active";

            //显示子菜单
            if (oUl[0]) {
                clearTimeout(hideTimer);
                showTimer = setTimeout(function () {
                    for (i = 0; i < oThis.parentNode.children.length; i++) {
                        oThis.parentNode.children[i].getElementsByTagName("ul")[0] &&
                        (oThis.parentNode.children[i].getElementsByTagName("ul")[0].style.display = "none");
                    }
                    oUl[0].style.display = "block";
                    oUl[0].style.top = oThis.offsetTop + "px";
                    oUl[0].style.left = oThis.offsetWidth + "px";
                    setWidth(oUl[0]);

                    //最大显示范围
                    maxWidth = aDoc[0] - oUl[0].offsetWidth;
                    maxHeight = aDoc[1] - oUl[0].offsetHeight;

                    //防止溢出
                    maxWidth < getOffset.left(oUl[0]) && (oUl[0].style.left = -oUl[0].clientWidth + "px");
                    maxHeight < getOffset.top(oUl[0]) && (oUl[0].style.top = -oUl[0].clientHeight + oThis.offsetTop + oThis.clientHeight + "px")
                }, 300);
            }
        };

        //鼠标移出
        aLi[i].onmouseout = function () {
            var oThis = this;
            var oUl = oThis.getElementsByTagName("ul");
            //鼠标移出样式
            oThis.className = oThis.className.replace(/\s?active/, "");

            clearTimeout(showTimer);
            hideTimer = setTimeout(function () {
                for (i = 0; i < oThis.parentNode.children.length; i++) {
                    oThis.parentNode.children[i].getElementsByTagName("ul")[0] &&
                    (oThis.parentNode.children[i].getElementsByTagName("ul")[0].style.display = "none");
                }
            }, 300);
        };
    }
    //自定义右键菜单
    document.oncontextmenu = function (event) {
        var event = event || window.event;
        oMenu.style.display = "block";
        oMenu.style.top = event.clientY + "px";
        oMenu.style.left = event.clientX + "px";
        setWidth(aUl[0]);

        //最大显示范围
        maxWidth = aDoc[0] - oMenu.offsetWidth;
        maxHeight = aDoc[1] - oMenu.offsetHeight;

        //防止菜单溢出
        oMenu.offsetTop > maxHeight && (oMenu.style.top = maxHeight + "px");
        oMenu.offsetLeft > maxWidth && (oMenu.style.left = maxWidth + "px");
        return false;
    };

    //取li中最大的宽度, 并赋给同级所有li
    function setWidth(obj) {
        maxWidth = 80;
        for (i = 0; i < obj.children.length; i++) {
            var oLi = obj.children[i];
            var iWidth = oLi.clientWidth - parseInt(oLi.currentStyle ? oLi.currentStyle["paddingLeft"] : getComputedStyle(oLi, null)["paddingLeft"]) * 2
            if (iWidth > maxWidth) maxWidth = iWidth;
        }
        for (i = 0; i < obj.children.length; i++) obj.children[i].style.width = maxWidth + "px";
    }

    y += document.body.scrollTop;
    x += document.body.scrollLeft;
    if ($(window).width() > 990) {
        x = x - $("#menu").width();
    }
    $("#rMenudataTree").css({"top": y + "px", "left": x + "px", "visibility": "visible"});
    $("body").bind("mousedown", dataTreeonBodyMouseDown);
}

function dataTreehideRMenu() {
    var rMenudataTree = $("#rMenudataTree");
    if (rMenudataTree) rMenudataTree.css({"visibility": "hidden"});
    $("body").unbind("mousedown", dataTreeonBodyMouseDown);
}

function dataTreeonBodyMouseDown(event) {
    if (!(event.target.id == "rMenu" || $(event.target).parents("#rMenudataTree").length > 0)) {
        rMenudataTree.css({"visibility": "hidden"});
    }
}

function addDiyDom(treeId, treeNode) {
    var spaceWidth = 15;
    var liObj = $("#" + treeNode.tId);
    var aObj = $("#" + treeNode.tId + "_a");
    var switchObj = $("#" + treeNode.tId + "_switch");
    var icoObj = $("#" + treeNode.tId + "_ico");
    var spanObj = $("#" + treeNode.tId + "_span");
    aObj.attr('title', '');
    aObj.append('<div class="divTd swich fnt" style="width:30%"></div>');
    var div = $(liObj).find('div').eq(0);
    //从默认的位置移除
    switchObj.remove();
    spanObj.remove();
    icoObj.remove();
    //在指定的div中添加
    div.append(switchObj);
    div.append(spanObj);
    // {#                //隐藏了层次的span#}
    // {#                var spaceStr = "<span style='height:1px;display: inline-block;width:" + (spaceWidth * treeNode.level) + "px'></span>";#}
    // {#                switchObj.before(spaceStr);#}
    //图标垂直居中
    icoObj.css("margin-top", "9px");
    switchObj.after(icoObj);
    var editStr = '';
    //宽度需要和表头保持一致
    editStr += '<div class="divTd" style="width:20%">' + (treeNode.types == null ? '' : treeNode.types ) + '</div>';
    editStr += '<div class="divTd" style="width:50%">' + (fixXss(treeNode.description)) + '</div>';
    aObj.append(editStr);
}

var dataTree, rMenudataTree;
//初始化列表
function queryHandler(zTreeNodes) {
    //初始化树
    var datetree_count = zTreeNodes.length;
    document.getElementById("datetree_count").innerHTML = "共有"+datetree_count+"个对象";
    $.fn.zTree.init($("#dataTree"), setting1, zTreeNodes);
    //添加表头
    var li_head = ' <li class="head"><a><div class="divTd" style="width:30%">名称(name)</div><div class="divTd" style="width:20%">类型(objectClass)</div>' +
        '<div class="divTd" style="width:50%">描述(description)</div></a></li>';
    var rows = $("#dataTree").find('li');
    if (rows.length > 0) {
        rows.eq(0).before(li_head)
    } else {
        $("#dataTree").append(li_head);
        $("#dataTree").append('<li ><div style="text-align: center;line-height: 30px;" >无符合条件数据</div></li>')
    }
    dataTree = $.fn.zTree.getZTreeObj("dataTree");
    rMenudataTree = $("#rMenudataTree");
}

//第2颗 finddataTree 搜索
$(document).ready(function () {
    fuzzySearch('dataTree', '#finddataTree', null, true); //初始化模糊搜索方法
});


//第3棵ztreeou 树,用来做移动到新OU
var setting_ou = {
    async: {
        enable: true, //表示异步加载生效
        url: "/show_ou_for_dn/",// 异步加载时访问的页面
        autoParam: ["distinguishedName", "id"], // 异步加载时自动提交的父节点属性的参数
        //otherParam:["paths"], //ajax请求时提交的参数
        type: 'post',
        dataType: 'json'
    },
    view: {
        expandSpeed: "",//zTree 节点展开、折叠时的动画速度
        selectedMulti: false ////设置是否允许同时选中多个节点。
    },
    data: {
        simpleData: {
            enable: true
        }
    },//设置数据格式为id
    check: {
        enable: false,//设置 zTree 的节点上是否显示 checkbox / radio
        chkStyle: "checkbox",
        chkboxType: {"Y": "s", "N": "s"},//只影响子节点
    },
};
$(document).ready(function () {
    startztree()
});
function startztree() {
    $.fn.zTree.init($("#treemove"), setting_ou, zNodes);//初始化zTree
    var ztreeou = $.fn.zTree.getZTreeObj("treemove");
    var nodes = ztreeou.getNodes();
    if (nodes.length > 0) {
        for (var i = 0; i < nodes.length; i++) {
            ztreeou.expandNode(nodes[i], true, false, false);//默认展开第一级节点
        }
    }
};

