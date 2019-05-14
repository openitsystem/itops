webpackJsonp([16],{

/***/ 1877:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__babel_loader_node_modules_vue_loader_13_7_3_vue_loader_lib_selector_type_script_index_0_computervaluemanagedby_vue__ = __webpack_require__(2199);
/* empty harmony namespace reexport */
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__node_modules_vue_loader_13_7_3_vue_loader_lib_template_compiler_index_id_data_v_0f965671_hasScoped_false_transformToRequire_video_src_poster_source_src_img_src_image_xlink_href_buble_transforms_node_modules_vue_loader_13_7_3_vue_loader_lib_selector_type_template_index_0_computervaluemanagedby_vue__ = __webpack_require__(2222);
function injectStyle (ssrContext) {
  __webpack_require__(2220)
  __webpack_require__(2221)
}
var normalizeComponent = __webpack_require__(31)
/* script */


/* template */

/* template functional */
var __vue_template_functional__ = false
/* styles */
var __vue_styles__ = injectStyle
/* scopeId */
var __vue_scopeId__ = null
/* moduleIdentifier (server only) */
var __vue_module_identifier__ = null
var Component = normalizeComponent(
  __WEBPACK_IMPORTED_MODULE_0__babel_loader_node_modules_vue_loader_13_7_3_vue_loader_lib_selector_type_script_index_0_computervaluemanagedby_vue__["a" /* default */],
  __WEBPACK_IMPORTED_MODULE_1__node_modules_vue_loader_13_7_3_vue_loader_lib_template_compiler_index_id_data_v_0f965671_hasScoped_false_transformToRequire_video_src_poster_source_src_img_src_image_xlink_href_buble_transforms_node_modules_vue_loader_13_7_3_vue_loader_lib_selector_type_template_index_0_computervaluemanagedby_vue__["a" /* default */],
  __vue_template_functional__,
  __vue_styles__,
  __vue_scopeId__,
  __vue_module_identifier__
)

/* harmony default export */ __webpack_exports__["default"] = (Component.exports);


/***/ }),

/***/ 2199:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_axios__ = __webpack_require__(88);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_axios___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_axios__);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



// import Vue from 'vue'
// import qs from 'qs'
__WEBPACK_IMPORTED_MODULE_0_axios___default.a.defaults.withCredentials = true;
/* harmony default export */ __webpack_exports__["a"] = ({
  data: function data() {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      changespanshow: {
        changecnshow: true
      },
      dialogVisible: false,
      loading: false,
      options4: [],
      value9: [],
      vLoadingShow: false, // 读条全屏遮罩
      managedBy: null, // managedBy管理者
      telephoneNumber: null, // 电话号码
      sAMAccountName: null, // 用户登录名
      cn: null, // 全名
      physicalDeliveryOfficeName: null, // 办公室
      mail: null, // 电子邮件
      tableData2: [{
        date: 'displayName'
      }]
    };
  },

  methods: {
    getmanagermessagevalue: function getmanagermessagevalue() {
      var _this = this;

      var loading = this.$loading({
        lock: true
      });
      var disNameforurl = this.getQueryVariable('disName');
      __WEBPACK_IMPORTED_MODULE_0_axios___default.a.get(this.serviceurl() + '/api/GetCompMessage/?CountName=' + disNameforurl).then(function (response) {
        loading.close();
        if (response.data.isSuccess) {
          _this.managedBy = response.data.message.managedBy;
          __WEBPACK_IMPORTED_MODULE_0_axios___default.a.get(_this.serviceurl() + '/api/GetUserMessage/?CountName=' + response.data.message.managedBy + '&objectClass=DN').then(function (response) {
            if (response.data.isSuccess) {
              _this.telephoneNumber = response.data.message.telephoneNumber;
              _this.sAMAccountName = response.data.message.sAMAccountName;
              _this.cn = response.data.message.cn;
              _this.physicalDeliveryOfficeName = response.data.message.physicalDeliveryOfficeName;
              _this.mail = response.data.message.mail;
            } else {
              if (response.data.message === '权限不足') {
                _this.messagealertvalue('权限不足', 'error');
              } else {
                _this.messagealertvalue('加载失败', 'error');
              }
            }
          }).catch(function () {
            this.messagealertvalue('加载失败', 'error');
          });
        } else {
          if (response.data.message === '权限不足') {
            _this.messagealertvalue('权限不足', 'error');
          } else {
            _this.messagealertvalue('加载失败', 'error');
          }
        }
      }).catch(function () {
        this.messagealertvalue('加载失败', 'error');
      });
    },
    savechangecn: function savechangecn() {
      console.log();
    },
    remoteMethod: function remoteMethod(query) {
      var _this2 = this;

      if (query !== '') {
        this.loading = true;
        __WEBPACK_IMPORTED_MODULE_0_axios___default.a.get(this.serviceurl() + '/api/GetOnlyConMessage/?username=' + query).then(function (response) {
          if (response.data.isSuccess) {
            _this2.options4 = response.data.message;
          } else {
            _this2.options4 = [];
          }
          _this2.loading = false;
        }).catch(function () {
          this.options4 = [];
          this.loading = false;
        });
      } else {
        this.options4 = [];
      }
    },
    changemanagergroup: function changemanagergroup() {
      var _this3 = this;

      this.loading = true;
      var disNameforurl = this.getQueryVariable('disName');
      __WEBPACK_IMPORTED_MODULE_0_axios___default.a.get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + disNameforurl + '&Attributes=managedBy&ChangeMessage=' + this.value9).then(function (response) {
        if (response.data.isSuccess) {
          _this3.messagealertvalue('修改成功', 'success');
          _this3.getmanagermessagevalue();
          _this3.dialogVisible = false;
        } else {
          if (response.data.message === '权限不足') {
            _this3.messagealertvalue('权限不足', 'error');
          } else {
            _this3.messagealertvalue('修改失败', 'error');
          }
        }
        _this3.loading = false;
      }).catch(function () {
        this.messagealertvalue('修改失败', 'error');
        this.loading = false;
      });
    }
  },
  created: function created() {
    this.getmanagermessagevalue();
  }
});

/***/ }),

/***/ 2220:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 2221:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 2222:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
var render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('el-col',{attrs:{"span":24}},[_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"managedBy","placement":"left-start"}},[_c('span',[_vm._v(" 管理者：")])]),_vm._v(" "),_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"修改管理者","placement":"top"}},[_c('span',{class:[_vm.classname.classSpanFloatRight,_vm.classname.classSpancursorpointer],staticStyle:{"font-size":"130%"},on:{"click":function($event){_vm.dialogVisible = true ,_vm.value9 = []}}},[_c('i',{staticClass:"el-icon-edit-outline"})])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.managedBy)}})]}}])})],1),_vm._v(" "),_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"telephoneNumber","placement":"left-start"}},[_c('span',[_vm._v(" 电话号码：")])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.telephoneNumber)}})]}}])})],1),_vm._v(" "),_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"sAMAccountName","placement":"left-start"}},[_c('span',[_vm._v(" 用户登录名：")])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.sAMAccountName)}})]}}])})],1),_vm._v(" "),_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"cn","placement":"left-start"}},[_c('span',[_vm._v(" 全名：")])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.cn)}})]}}])})],1),_vm._v(" "),_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"physicalDeliveryOfficeName","placement":"left-start"}},[_c('span',[_vm._v(" 办公室：")])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.physicalDeliveryOfficeName)}})]}}])})],1),_vm._v(" "),_c('el-table',{staticStyle:{"width":"100%"},attrs:{"data":_vm.tableData2,"show-header":false}},[_c('el-table-column',{attrs:{"width":"180"},scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('el-tooltip',{staticClass:"item",attrs:{"effect":"light","content":"mail","placement":"left-start"}},[_c('span',[_vm._v(" 电子邮件：")])])]}}])}),_vm._v(" "),_c('el-table-column',{scopedSlots:_vm._u([{key:"default",fn:function(scope){return [_c('span',{domProps:{"textContent":_vm._s(_vm.mail)}})]}}])})],1),_vm._v(" "),_c('el-dialog',{attrs:{"title":"更改管理者","visible":_vm.dialogVisible,"width":"60%","center":""},on:{"update:visible":function($event){_vm.dialogVisible=$event}}},[_c('el-select',{staticStyle:{"width":"90%"},attrs:{"multiple":"","filterable":"","remote":"","multiple-limit":1,"placeholder":"请输入管理者关键信息","remote-method":_vm.remoteMethod,"loading":_vm.loading},model:{value:(_vm.value9),callback:function ($$v) {_vm.value9=$$v},expression:"value9"}},_vm._l((_vm.options4),function(item){return _c('el-option',{key:item.sAMAccountName,attrs:{"label":item.sAMAccountName + ' (' + item.displayName + ')',"value":item.distinguishedName}})}),1),_vm._v(" "),_c('span',{staticClass:"dialog-footer",attrs:{"slot":"footer"},slot:"footer"},[_c('el-button',{on:{"click":function($event){_vm.dialogVisible = false}}},[_vm._v("取 消")]),_vm._v(" "),_c('el-button',{attrs:{"type":"primary"},on:{"click":_vm.changemanagergroup}},[_vm._v("确 定")])],1)],1)],1)}
var staticRenderFns = []
var esExports = { render: render, staticRenderFns: staticRenderFns }
/* harmony default export */ __webpack_exports__["a"] = (esExports);

/***/ })

});