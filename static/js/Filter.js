
/**
 * edatagrid - jQuery EasyUI
 * 
 * Licensed under the GPL:
 *   http://www.gnu.org/licenses/gpl.txt
 *
 * Copyright 2011-2015 www.jeasyui.com 
 * 
 * Dependencies:
 *   datagrid
 *   messager
 * 
 */
(function ($) {
    //初始化绑定事件
    $(function () {
       
    });
    $.fn.extend({
        comboboxfilter: function (ops) {
            if (typeof (arguments[0]) != typeof ("string")) {
                return $.fn.comboboxfilter.methods["init"](this, ops);
            } else {
                return $.fn.comboboxfilter.methods[arguments[0]](this, arguments);
            }
        }
    });

    //方法
    $.fn.comboboxfilter.methods = {
        options: function (target) {
            var opts = $(target).data("comboboxfilter").options;
            return opts;
        },
        init: function (target, ops) {
            var $this = this;
            var options = $.extend({}, $.fn.comboboxfilter.defaults, ops);
            $(target).data("comboboxfilter", { options: options });
            $(target).removeClass('hotel-filter-list filter-list-has-more hotel-filter-list-min').addClass("hotel-filter-list filter-list-has-more hotel-filter-list-min");
            var listcontainer = $('<div class="con"></div>').addClass(!options.multiple ? "radio" : "checkbox");
            if (options.unlimit) {//如果开启不限 则添加 
                var anyNode = $('<ul class="any"><li><a class="filter-unlimit filter-tag selected" href="javascript:;" data-value="">' + options.unlimitText + '</a></li></ul>').bind('click',function() {
                    $(anyNode).find('.filter-unlimit').removeClass('selected').addClass('selected');
                    $this.clear(target);
                });
                listcontainer.append(anyNode);
            }
            listcontainer.append('<ul class="list "></ul> ');
            listcontainer.find('.open').unbind('click').bind('click', function() {//绑定点击更多事件
                $(target).removeClass('hotel-filter-list-min');
            });
            listcontainer.find('.close').unbind('click').bind('click', function () {//绑定点击更多事件
                $(target).addClass('hotel-filter-list-min');
            });
            $(target).html($('<strong class="tit">' + options.text + '</strong>'));
            if (options.inputName) {//添加隐藏的inputName
                $(target).append($('<input type="hidden" name="' + options.inputName + '" value="">'));
            }
            //具有分组
            if (options.scope) {
                $(target).attr('scope', options.scope);//添加自定义分组属性
                if ($('#' + options.scope).length>0) {
                    
                } else {
                    var node = $('<div id="' + options.scope + '" class="hotel-filter-list "><strong class="tit">已选</strong><div class="con selected-query"><ul  class="list"><li class="filter-query-clear"><a class="J_FilterQueryClear" href="javascript:;">清除</a></li></ul></div></div>');
                    node.find('.J_FilterQueryClear').unbind('click').bind('click',function() {//全部清除事件
                        $('div[scope="' + options.scope + '"]').comboboxfilter('clear');
                    });
                    $('div[scope="' + options.scope + '"]:eq(0)').before(node);
                }
            }
            $(target).append(listcontainer);
            this.load(target,{});

        },
        reload: function (target) {
            this.load(target,{});
        },
        load: function (target, opts) {
            var $this = this;
            var options = $.extend({}, $.fn.comboboxfilter.methods["options"](target), opts);
            if (opts.url) {
                $.ajax({
                    type: 'post',
                    data: options.param,
                    url: options.url,
                    success: function(data) {
                        if (typeof (data) == typeof ("string")) {
                            data = $.parseJSON(data);
                        }
                        var listTarget = $(target).find('.list').html('');
                        $this.setData(listTarget, options, data, target);
                    },
                    error: function(e) {
                        $this.onError(e);
                    }
                });
            } else {
                var listTarget = $(target).find('.list').html('');
                $this.setData(listTarget, options, options.data, target);
            }
            
        },
        loadData: function (target, data) {
            var $this = this;
            var options = $this.options(target);
            var listTarget = $(target).find('.list').html('');
            $this.setData(listTarget, options, data, target);

        },
        setData: function (target, options, data, targetContain) {
            var $this = this;
            $.each(data, function (i, item) {
                var listnode = $(' <li></li>');
                var clicka = $('<a class="filter-tag" href="javascript:;" data-value="' + item[options.idField] + '" data-text="' + item[options.textField] + '">' + item[options.textField] + '</a>').data('data', item);
                clicka.unbind('click').bind('click', function (e) {
                    if (clicka.hasClass('selected')) {//验证是否被选择，已经选择则取消选择，反之选择
                        clicka.removeClass('selected');//不可去掉（为了计算Value的正确性）
                    } else {
                        if (!options.multiple) {//单选执行
                            $(targetContain).find('.selected').trigger("click.selected-tag");//触发事件清除全部选项
                        }
                        clicka.addClass('selected');
                        $this.addSelected($('#' + options.scope), clicka, item, options, targetContain);//容器中添加选择项
                    }
                    $this.reSetValue(targetContain); //重新计算Value
                    options.onClick(item);//触发单机事件
                });
                listnode.append(clicka);
                target.append(listnode);
            });
            options.onLoadSuccess(data);//触发加载完成事件
        },
        getValue: function(target) {
            var selected = $(target).find('.list .selected');
            var array = new Array();
            $.each(selected, function(i,item) {
                array.push($(item).attr('data-value'));
            });
            return array.join(",");
        },
        setValue: function (target, value) {
            $(target).find('.selected').trigger("click.selected-tag");//触发事件清除全部选项用于重新赋值
            var options = this.options(target);
            var clicka = $(target).find('.filter-tag[data-value="' + value[1] + '"]');
            if (clicka.length > 0) {
                clicka.addClass('selected');
                var item = $(clicka).data('data');//取值
                this.addSelected($('#' + options.scope), clicka, item, options, target);//容器中添加选择项
            }
            this.reSetValue(target); //重新计算Value
        },
        setValues: function (target, valueArray) {
            var $this = this;
            var options = this.options(target);
            if (options.multiple) {//开启多选可用
                $(target).find('.selected').trigger("click.selected-tag");//触发事件清除全部选项用于重新赋值
                $.each(valueArray[1], function (i, itemData) {
                    var clicka = $(target).find('.filter-tag[data-value="' + itemData + '"]');
                    if (clicka.length > 0) {
                        clicka.addClass('selected');
                        var item = $(clicka).data('data');//取值
                        $this.addSelected($('#' + options.scope), clicka, item, options, target);//容器中添加选择项
                    }
                });
                $this.reSetValue(target); //重新计算Value
            }
        },
        //添加已经选择项
        //pointTarget：选择项容器
        //target 被点击的项
        //itemData 被选择数据
        addSelected: function (pointTarget, target, itemData, options, targetContain) {
            var $this = this;
          var anode = $('<a href="javascript:;">' + itemData[options.textField] + '</a>');
                //创建X ,点击则移除选择项
                var inode = $('<i class="J_FilterQueryDel" data-type="ParentCatelog" data-value="' + itemData[options.idField] + '"></i>').unbind('click').bind('click', function (e) {
                    $(target).trigger("click.selected-tag");//触发事件
                   // $(e.target).closest('.selected-tag').remove();
                    $this.reSetValue(targetContain); //重新计算Value
                });
                //绑定指定命名空间的单击事件
                $(target).unbind('click.selected-tag').bind('click.selected-tag', function (e) {
                    $(target).removeClass('selected');
                    $(anode).closest('.selected-tag').remove();
                    $(target).unbind('click.selected-tag');
                });
                anode.append(inode);
                pointTarget.find('.list').append($('<li data-type="ParentCatelog" class="selected-tag"></li>').append(anode));
        },
        //重新计算Value
        reSetValue: function (target) {
            var value = this.getValue(target);
            $(target).find('input[name="' + this.options(target).inputName + '"]').val(value);
            //有值
            if (value) {
                $(target).find('.filter-unlimit').removeClass('selected');
            }
            //无值
            else {
                $(target).find('.filter-unlimit').addClass('selected');
            }
            this.options(target).onChange(value);
        },
        clear: function (target) {
            $(target).find('.selected').trigger("click.selected-tag");//触发事件
            this.reSetValue(target); //重新计算Value
        }
    }
    $.fn.comboboxfilter.parseOptions = function (target) {
        return $.extend({}, $.fn.datagrid.parseOptions(target), {
        });
    };
   
    $.fn.comboboxfilter.defaults = {
        url: '',	
        idField: 'id',
        textField: 'text',
        scope: 'FilterQuery',
        text: '',
        multiple: false,
	data:[],
        inputName: '',
        unlimit: true,//是否显示不限，默认显示
        unlimitText:'标签',
        param:{},
        onClick: function (itemData) { },
        onChange: function (newValue) { },
        onLoadSuccess: function (data) { },
        onError: function (e) { }
    };
})(jQuery);