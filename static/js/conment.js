$(function(){
    $('#startchange').hide();
});
$.contextMenu({
    // define which elements trigger this menu
    selector: "#table tbody tr.conttext",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);

            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/contactvalue/?disName='+encodeURIComponent(this.context.childNodes[5].innerText))

            }
        },
    },

});//联系人
$.contextMenu({
    // define which elements trigger this menu
    selector: "#table tbody tr.contcomputercont",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);

            }
        },
        firs: {
            name: "添加到组(G)",
            callback: function (key, opt) {
                addusertosro(this.context.childNodes[0].innerText)
            }
        },
        sercon: {
            name: "启用账户(S)",
            callback: function (key, opt) {
                disenbaleuser(this.context.childNodes[5].innerText,this.context.childNodes[6].innerText)
            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/computervalue/?disName='+this.context.childNodes[0].innerText)

            }
        },
    },

});//计算机禁用
$.contextMenu({
    // define which elements trigger this menu

    selector: "#table tbody tr.contcomputer",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);

            }
        },
        firs: {
            name: "添加到组(G)",
            callback: function (key, opt) {
                addusertosro(this.context.childNodes[0].innerText)
            }
        },
        sercon: {
            name: "禁用账户(S)",
            callback: function (key, opt) {
                enbaleuser(this.context.childNodes[5].innerText,this.context.childNodes[6].innerText);
            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/computervalue/?disName='+this.context.childNodes[0].innerText)


            }
        },
    },

});//计算机启用
$.contextMenu({
    // define which elements trigger this menu

    selector: "#table tbody tr.contusercont",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);

            }
        },
        bar: {
            name: "重置密码(E)", callback: function (key, opt) {
                showResetPassword(this.context.childNodes[5].innerText,this.context.childNodes[0].innerText,this.context.childNodes[7].innerText);
                console.log(this.context)
            }
        },
        firs: {
            name: "添加到组(G)",
            callback: function (key, opt) {
                addusertosro(this.context.childNodes[0].innerText)
            }
        },
        sercon: {
            name: "启用账户(S)",
            callback: function (key, opt) {
                disenbaleuser(this.context.childNodes[5].innerText,this.context.childNodes[6].innerText)
            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/searchuser/?disName='+this.context.childNodes[0].innerText)
            }
        },
    },

});//用户禁用
$.contextMenu({
    // define which elements trigger this menu

    selector: "#table tbody tr.contuser",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);

            }
        },
        bar: {
            name: "重置密码(E)", callback: function (key, opt) {
                showResetPassword(this.context.childNodes[5].innerText,this.context.childNodes[0].innerText,this.context.childNodes[7].innerText);
                console.log(this.context)
            }
        },
        firs: {
            name: "添加到组(G)",
            callback: function (key, opt) {
                addusertosro(this.context.childNodes[0].innerText)
            }
        },
        sercon: {
            name: "禁用账户(S)",
            callback: function (key, opt) {
                enbaleuser(this.context.childNodes[5].innerText,this.context.childNodes[6].innerText);
            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/searchuser/?disName='+this.context.childNodes[0].innerText)
            }
        },
    },

});//用户启用
$.contextMenu({
    // define which elements trigger this menu
    selector: "#table tbody tr.contgroup",
    // define the elements of the menu
    items: {
        foo: {
            name: "移动(V)",
            callback: function (key, opt) {
                startztree();
                moveUSER(this.context.childNodes[5].innerText);
            }
        },
        for: {
            name: '添加成员(A)',
            callback: function (key, opt) {
                addgroupuser(this.context.childNodes[0].innerText)
            }
        },
        bar: {
            name: "导出(D)", callback: function (key, opt) {
                exportexcel(this.context.childNodes[5].innerText,this.context.childNodes[0].innerText);
            }
        },
        three: {
            name: '属性(R)',

            callback: function (key, opt) {
                openModle('/groupvalue/?disName='+this.context.childNodes[0].innerText)
            }
        },
    },
});//组
// there's more, have a look at the demos and docs...
//导出

function searchmessage(){
    idtype =  document.getElementById("idtype").value;
    if (idtype=='searc'){
        adaccount =  document.getElementById("adaccount").value;
        sele =  document.getElementById("sele").value;
        if(adaccount==''){
            swal('账号不能为空');
            return false
        }
        else {
            var bh = $("body").height();
            var bw = $("body").width();
            $("#fullbg").css({
                height: bh+350,
                width: bw,
                display: "block"
            });
            $("#dialoga").show();
            $.ajax({
                // url:'{% url "api:GetConMessage" %}',
                // url:'{% url "api:GetConMessage" %}',
                //  url: '{% url "showmailgroup" %}',
                // url:'{% url api:GetConMessage %}',
                url:"/api/GetConMessage/" ,
                type:'POST',
                dataType:'json',

                traditional:true,
                data:{"username":adaccount,"mode":sele},
                success:function (data) {
                    $("#startchange").show();
                    $("#searchuser").html('');
                    if (data['isSuccess']){
                        if (data['count']!='0'){
                            document.getElementById('counts').innerText = '  ---找到'+data['count']+'个项目';
                            for (i = 0; i < data['message'].length; i++) {
                                if (data['message'][i]['objectClass']=='用户'){
                                    if (data['message'][i]['userAccountConte']=='启用') {
                                        newRow = "<tr class='contuser' ondblclick=\"openModle('/searchuser/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+data['message'][i]['objectClass']+"</td><td>"+data['message'][i]['distinguishedName']+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['lockoutTime'])+"</td></tr>"
                                    }
                                    else {
                                        newRow = "<tr class='contusercont' ondblclick=\"openModle('/searchuser/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+data['message'][i]['objectClass']+"</td><td>"+data['message'][i]['distinguishedName']+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['lockoutTime'])+"</td></tr>"
                                    }
                                }
                                else if(data['message'][i]['objectClass']=='组'){
                                    newRow = "<tr class='contgroup' ondblclick=\"openModle('/groupvalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                                }
                                else if(data['message'][i]['objectClass']=='联系人'){
                                    newRow = "<tr class='conttext'ondblclick=\"openModle('/contactvalue/?disName="+ encodeURIComponent(data['message'][i]['distinguishedName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                                }
                                else if(data['message'][i]['objectClass']=='计算机'){
                                    if (data['message'][i]['userAccountConte']=='启用') {
                                        newRow = "<tr class='contcomputer' ondblclick=\"openModle('/computervalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td></tr>"
                                    }
                                    else {
                                        newRow = "<tr class='contcomputercont' ondblclick=\"openModle('/computervalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) +"')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td >"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td></tr>"
                                    }
                                }
                                else {
                                    newRow = "<tr class='contxtxtx'><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                                }
                                $("#searchuser").append(newRow);
                            }
                        }
                        else {
                            document.getElementById('counts').innerText = '  ---找到0个项目';
                            newRow="<tr><td colspan='5'>未查询到账号信息</td></tr>";
                            $("#searchuser").append(newRow);
                        }
                    }
                    else {
                        newRow="<tr><td colspan='5'>搜索出现异常</td></tr>";
                        $("#searchuser").append(newRow);
                    }
                    $("#fullbg,#dialoga").hide();
                    $("#table").resizableColumns({
                        store: window.store
                    });
                }
            });
        }
    }
    else {
        searchvalue =  document.getElementById("adaccount").value;
        NameList=[];
        $("#spanvalueid h5 option:selected").each(function(){
            NameList.push($(this).val())
        });
        var bh = $("body").height();
        var bw = $("body").width();
        $("#fullbg").css({
            height: bh+20,
            width: bw,
            display: "block"
        });
        $("#dialoga").show();
        $.ajax({
            // url:'{% url "api:GetLeaveUser" %}',
            url:"/api/GetLeaveUser/" ,
            type: 'POST',
            dataType: 'json',
            traditional: true,
            data: {'searchvalue': searchvalue, 'NameList': NameList},
            success: function (data) {
                $("#startchange").show();
                $("#searchuser").html('');
                if (data['isSuccess']){
                    if (data['count']!='0'){
                        document.getElementById('counts').innerText = '  ---找到'+data['count']+'个项目';
                        for (i = 0; i < data['message'].length; i++) {
                            if (data['message'][i]['objectClass']=='用户'){
                                if (data['message'][i]['userAccountConte']=='启用') {
                                    newRow = "<tr class='contuser' ondblclick=\"openModle('/searchuser/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+data['message'][i]['objectClass']+"</td><td>"+data['message'][i]['distinguishedName']+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['lockoutTime'])+"</td></tr>"
                                }
                                else {
                                    newRow = "<tr class='contusercont' ondblclick=\"openModle('/searchuser/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+data['message'][i]['objectClass']+"</td><td>"+data['message'][i]['distinguishedName']+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['lockoutTime'])+"</td></tr>"
                                }
                            }
                            else if(data['message'][i]['objectClass']=='组'){
                                newRow = "<tr class='contgroup' ondblclick=\"openModle('/groupvalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                            }
                            else if(data['message'][i]['objectClass']=='联系人'){
                                newRow = "<tr class='conttext' ondblclick=\"openModle('/contactvalue/?disName="+ encodeURIComponent(data['message'][i]['distinguishedName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                            }
                            else if(data['message'][i]['objectClass']=='计算机'){
                                if (data['message'][i]['userAccountConte']=='启用') {
                                    newRow = "<tr class='contcomputer' ondblclick=\"openModle('/computervalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) + "')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td></tr>"
                                }
                                else {
                                    newRow = "<tr class='contcomputercont' ondblclick=\"openModle('/computervalue/?disName="+ fixXss(data['message'][i]['sAMAccountName']) +"')\"><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td >"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td><td style='display:none'>"+fixXss(data['message'][i]['userAccountControl'])+"</td></tr>"
                                }
                            }
                            else {
                                newRow = "<tr class='contxtxtx'><td style='display:none'>"+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+data['message'][i]['icon']+fixXss(data['message'][i]['sAMAccountName'])+"</td><td>"+fixXss(data['message'][i]['displayName'])+"</td><td>"+fixXss(data['message'][i]['description'])+"</td><td>"+fixXss(data['message'][i]['objectClass'])+"</td><td>"+fixXss(data['message'][i]['distinguishedName'])+"</td></tr>"
                            }
                            $("#searchuser").append(newRow);
                        }
                    }
                    else {
                        document.getElementById('counts').innerText = '  ---找到'+data['count']+'个项目';
                        newRow="<tr><td colspan='5'>未查询到账号信息</td></tr>";
                        $("#searchuser").append(newRow);
                    }
                }
                else {
                    newRow="<tr><td colspan='5'>搜索出现异常</td></tr>";
                    $("#searchuser").append(newRow);
                }
                $("#fullbg,#dialoga").hide();
                $("#table").resizableColumns({
                    store: window.store
                });
            }
        });

    }}


//设置垂直滚动条
$(document).ready(function () {
    $('#paneltable').slimScroll({
        color: '#eee',
        size: '5px',
        height: $(document.body).height(),
        alwaysVisible: true
    });
});

function exportexcel(dn,name) {
    post_url = '/groupexport/?filter='+dn+'&samename='+name;
    location.replace(post_url);
}
$("#adaccount").keydown(function (e) {
    if (e.keyCode==13){
        searchmessage()
    }
});
$('#selsgroup').select2({
    minimumInputLength: 1,//最少输入多少个字符后开始查询
    language: "zh-CN",
    ajax: {
        type:'GET',
        //url:'{% url "api:GetGroupAnrMessage" %}',
        url:"/api/GetGroupAnrMessage/" ,
        dataType: 'json',
        data: function (params) {
            return {
                CountName: params.term, // search term 请求参数 ， 请求框中输入的参数
            };
        },
        processResults:function (data) {
            allmessage=[];
            if (data['isSuccess']){
                for (i = 0; i < data['message'].length; i++) {
                    mess={'id':data['message'][i]['sAMAccountName'],'text':data['message'][i]['cn']};
                    allmessage.push(mess);
                }
                return {
                    results: allmessage  //必须赋值给results并且必须返回一个obj
                };
            }
            else{
                swal(data['message'])
            }
        }
    },
});
$('#selsusergroup').select2({
    minimumInputLength: 2,//最少输入多少个字符后开始查询
    language: "zh-CN",
    ajax: {
        type:'GET',
        // url:'{% url "api:GetOnlyConMessage" %}',
        url:"/api/GetOnlyConMessage/" ,
        dataType: 'json',
        data: function (params) {
            return {
                username: params.term, // search term 请求参数 ， 请求框中输入的参数
            };
        },
        processResults:function (data) {
            allmessage=[];
            if (data['isSuccess']){
                for (i = 0; i < data['message'].length; i++) {
                    mess={'id':data['message'][i]['sAMAccountName'],'text':data['message'][i]['cn']+'('+data['message'][i]['displayName']+')'};
                    allmessage.push(mess);
                }
                return {
                    results: allmessage  //必须赋值给results并且必须返回一个obj
                };
            }
            else{
                swal(data['message'])
            }
        }
    },
});
function saveusertogroup() {
    strtext = $("#selsgroup").select2("val");
    disName = document.getElementById("snamsuser").value;
    $.ajax({
        //  url:'{% url "api:AddUserToGroup" %}',
        url:"/api/AddUserToGroup/" ,
        type:'GET',
        dataType:'json',
        async: false,
        traditional:true,
        data:{"CountName":disName,"GdisNameList":strtext},
        success:function (data) {
            if (data['isSuccess']) {
                swal({
                        title:"",
                        text:"添加到组成功",
                        type:"success",
                        showConfirmButton:"true",
                        confirmButtonText:"好的",
                        animation:"slide-from-top"
                    },
                    function () {
                        $("#addusretoModal").modal("hide");
                        $("#selsgroup").select2("val", " ");
                    })
            }
            else {
                swal(data['message'])
            }
        }
    })
}
function savegroupuseron() {
    strtext = $("#selsusergroup").select2("val");
    disName = document.getElementById("snamsusercouny").value;
    $.ajax({
        //url:'{% url "api:AddGroupsTo" %}',
        url:"/api/AddGroupsTo/" ,
        type:'GET',
        dataType:'json',
        async: false,
        traditional:true,
        data:{"GroupName":disName,"GdisNameList":strtext},
        success:function (data) {
            if (data['isSuccess']) {
                swal({
                        title:"",
                        text:"添加成员成功",
                        type:"success",
                        showConfirmButton:"true",
                        confirmButtonText:"好的",
                        animation:"slide-from-top"
                    },
                    function () {
                        $("#addgroupuserModal").modal("hide");
                        $("#selsusergroup").select2("val", " ");
                    })
            }
            else {
                swal(data['message'])
            }
        }
    })
}


function moveUSER(userdnames) {
    document.getElementById('oudnname').value='';
    document.getElementById('userdnname').value=userdnames;
    $('#myModamove').modal({
        keyboard: true,
    });
}
function addusertosro(sancount) {
    $("#selsgroup").select2("val", " ");
    document.getElementById('snamsuser').value=sancount;
    $('#addusretoModal').modal({
        keyboard: true,
    });
}

window.onload = function(){
    tableCont = document.querySelector('#paneltable');
    /**
     * scroll handle
     * @param {event} e -- scroll event
     */
    function scrollHandle (e){
        scrollTop = this.scrollTop;
        this.querySelector('thead').style.transform = 'translateY(' + scrollTop + 'px)';
    }
    tableCont.addEventListener('scroll',scrollHandle)
};


setting = {
    async: {
        enable: true, //表示异步加载生效
        //url:{% url "show_ou_for_dn" %},// 异步加载时访问的页面
        url:"/show_ou_for_dn/" ,
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
    },
};
$.ajax({
    //url: {% url "show_domain" %},
    url:"/show_domain/" ,
    type: 'POST',
    dataType: 'json',
    async: false,
    success: function (data) {
        zNodes = data["message"];
    }
});//生成OU初始数

//点击事件
function zTreeOnClick() {
    var zTree = $.fn.zTree.getZTreeObj("treemove"), //zTree = Object {setting: Object} 根据 treeId 获取 zTree 对象的方法
        nodes = zTree.getSelectedNodes(), // nodes = [Object] 获取zTree当前被选中的节点数据集合
        treeNode = nodes[0];
    document.getElementById('oudnname').value=treeNode.distinguishedName;
}
var zTree,zNodes;
$(document).ready(function () {
    startztree()
});
function startztree() {
    $.fn.zTree.init($("#treemove"), setting, zNodes);//初始化zTree
    zTree = $.fn.zTree.getZTreeObj("treemove");
    var nodes = zTree.getNodes();
    if (nodes.length>0){
        for(var i=0;i<nodes.length;i++){
            zTree.expandNode(nodes[i], true, false, false);//默认展开第一级节点
        }
    }
}


function savemovetoou() {
    uservaluedn = document.getElementById("userdnname").value;
    ouvaluedn = document.getElementById("oudnname").value;
    if (uservaluedn=='' || ouvaluedn==''){
        swal('请选中OU')
    }
    else {
        $.ajax({
            //url: {% url "setObjectMoveToOu" %},
            url:"/setObjectMoveToOu/" ,
            type: 'POST',
            dataType: 'json',
            data: {'dn': uservaluedn, 'new_superior': ouvaluedn,},
            success: function (data) {
                if (data['isSuccess']) {
                    swal({
                            title:"",
                            text:"移动成功",
                            type:"success",
                            showConfirmButton:"true",
                            confirmButtonText:"好的",
                            animation:"slide-from-top"
                        },
                        function () {
                            $("#myModamove").modal("hide");
                            searchmessage()
                        })
                } else {
                    swal("移动失败：" + data['message']);
                }
            }
        });
    }

}

function disenbaleuser(disName,uscountid) {
    var newusercoutd=parseInt(uscountid)-2;
    $.ajax({
        //url:'{% url "api:ChangeUserMessage" %}',
        url:"/api/ChangeUserMessage/" ,
        type:'POST',
        dataType:'json',
        async: false,
        traditional:true,
        data:{"disName":disName,"Attributes":'userAccountControl',"ChangeMessage":newusercoutd,},
        success:function (data) {
            if (data['isSuccess']) {
                swal({
                        title:"",
                        text:"启用成功",
                        type:"success",
                        showConfirmButton:"true",
                        confirmButtonText:"好的",
                        animation:"slide-from-top"
                    },
                    function () {
                        searchmessage()
                    })
            }
            else {
                swal(data['message'])
            }
        }
    })
}
function enbaleuser(disName,uscountid) {
    var newusercoutd=parseInt(uscountid)+2;
    $.ajax({
        // url:'{% url "api:ChangeUserMessage" %}',
        url:"/api/ChangeUserMessage/" ,
        type:'POST',
        dataType:'json',
        async: false,
        traditional:true,
        data:{"disName":disName,"Attributes":'userAccountControl',"ChangeMessage":newusercoutd,},
        success:function (data) {
            if (data['isSuccess']) {
                swal({
                        title:"",
                        text:"禁用成功",
                        type:"success",
                        showConfirmButton:"true",
                        confirmButtonText:"好的",
                        animation:"slide-from-top"
                    },
                    function () {
                        searchmessage()
                    })
            }
            else {
                swal(data['message'])
            }
        }
    })
}
function addgroupuser(disname) {
    $("#selsusergroup").select2("val", "");
    document.getElementById('snamsusercouny').value=disname;
    $('#addgroupuserModal').modal({
        keyboard: true,
    });
}