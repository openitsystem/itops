<template>
  <el-col :span="24">
  <el-menu style="margin-bottom:10px;height:60px" class="el-menu-demo" mode="horizontal">
    <!-- <el-menu-item> -->
        <el-button
          type="primary"
          style="margin-top:15px;margin-left:15px"
          size="small"
          @click="addGroup">添加群组</el-button>
        <el-button
          type="info"
          style="margin-top:15px;margin-left:15px"
          size="small"
          @click="exportExcel">导出列表</el-button>
        <el-button
          size="small"
          v-if="tableData3.length"
          type="danger"
          @click="removemoregroupfromuser">退出选中群组</el-button>
        <el-button
          type="text"
          style="margin-top:15px;margin-right:15px;cursor:default;float:right"
          @click="passfunction">总计：{{ tableData3.length }}</el-button>
  </el-menu>

  <!-- <el-button
    size="mini"
    @click="addGroup">添加群组</el-button>
  <el-button
    size="mini"
    v-if="tableData3.length"
    @click="exportExcel">导出列表</el-button>
  <el-button
    v-if="tableData3.length"
    size="mini">总计：{{ tableData3.length }}</el-button>
  <el-button
    size="mini"
    v-if="tableData3.length"
    type="danger"
    @click="removemoregroupfromuser">退出选中群组</el-button> -->
  <el-table id="selectusermemberoftable" @selection-change="selectionchangedvalue" height='500' :data="tableData3.filter(data => !search || data.date.toLowerCase().includes(search.toLowerCase()))" @row-dblclick="dataBackFillGoods" style="width: 100%" v-cloak>
    <el-table-column type="selection" v-if="tableData3.length">
    </el-table-column>
    <el-table-column label="名称" prop="name">
    </el-table-column>
    <el-table-column label="DN" prop="date">
    </el-table-column>
    <el-table-column
      align="right">
      <template slot="header"  slot-scope="scope">
        <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
      </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="danger"
          @click="Deletegroup(scope.$index, scope.row)">退出群组</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
    title="添加群组"
    :visible.sync="dialogVisible"
    width="60%"
    center>
    <p>
      <el-input
        type="textarea"
        :autosize="{ minRows: 2, maxRows: 6}"
        placeholder="批量搜索，请以英文“;”分隔"
        style="width: 70%"
        v-model="textarea3">
      </el-input>
      &nbsp;&nbsp;
      <el-button type="info" @click="serarchgroupvalue()" size="mini">检查名称</el-button>
    </p>
    <el-select
    v-model="value9"
    multiple
    filterable
    remote
    placeholder="请输入群组关键信息"
    :remote-method="remoteMethod"
    :loading="loading"
    style="width: 90%">
      <el-option
        v-for="item in options4"
        :key="item.sAMAccountName"
        :label="item.cn"
        :value="item.sAMAccountName">
      </el-option>
    </el-select>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="addgrouptrue">确 定</el-button>
    </span>
  </el-dialog>
</el-col>
</template>
<style>
  /* 向右浮动 */
  .classSpanFloatRight{
      float: right;
  }
  /* 鼠标放上去显示手形 */
  .classSpancursorpointer{
      cursor: pointer;
  }
</style>
<script>

import axios from 'axios'
// import Vue from 'vue'
// import qs from 'qs'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'
axios.defaults.withCredentials = true
export default{
  data () {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classmarginauto: 'classmarginauto'
      },
      search: '',
      multipleSelection: [],
      sAMAccountName: null,
      textarea3: null,
      vLoadingShow: false, // 读条全屏遮罩
      dialogVisible: false, // 模态框是否显示
      tableData3: [],
      options4: [],
      value9: [],
      loading: false
    }
  },
  created: function () {
    this.findgroupmembers()
  },
  methods: {
    passfunction () {},
    removemoregroupfromuser () {
      let disNameforurl = this.getQueryVariable('disName')
      if ((this.multipleSelection).length === 0) {
        this.messagealertvalue('请至少勾选一个群组', 'error')
      } else {
        let allmultipleSelectionvaluelist = ''
        for (let i = 0; i < this.multipleSelection.length; i++) {
          allmultipleSelectionvaluelist = allmultipleSelectionvaluelist + '&UserMembers=' + this.multipleSelection[i]['date']
        }
        const loading = this.$loading({
          lock: true
        })
        axios.get(this.serviceurl() + '/api/EmUserGroup/?CountName=' + disNameforurl + allmultipleSelectionvaluelist)
          .then(response => {
            loading.close()
            if (response.data.isSuccess) {
              this.messagealertvalue('修改成功', 'success')
              Object.assign(this.$data, this.$options.data())
              this.findgroupmembers()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('修改失败', 'error')
                Object.assign(this.$data, this.$options.data())
                this.findgroupmembers()
              }
            }
          })
      }
    },
    selectionchangedvalue (val) {
      this.multipleSelection = val
    },
    exportExcel () {
      let disNameforurl = this.getQueryVariable('disName')
      /* generate workbook object from table */
      let wb = XLSX.utils.table_to_book(document.querySelector('#selectusermemberoftable'))
      /* get binary string as output */
      let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
      try {
        FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), disNameforurl + '隶属于.xlsx')
      } catch (e) {
        this.messagealertvalue('导出失败', 'error')
      }
      return wbout
    },
    async serarchgroupvalue () {
      let textarea3lastvalue = ''
      let groupvaluelist = []
      if (this.textarea3 === null || this.textarea3 === '') {
        this.messagealertvalue('请输入有效值', 'error')
      } else {
        textarea3lastvalue = this.textarea3.replace(/ |\n/g, '') + ';'
        if (textarea3lastvalue === null || textarea3lastvalue === '') {
          this.messagealertvalue('请输入有效值', 'error')
        } else {
          let textarea3lastvaluelistvalue = textarea3lastvalue.split(';')
          for (let i = 0; i < textarea3lastvaluelistvalue.length; i++) {
            if (textarea3lastvaluelistvalue[i] !== '' && textarea3lastvaluelistvalue[i] !== null) {
              groupvaluelist.push(textarea3lastvaluelistvalue[i])
            }
          }
          if (groupvaluelist.length === 0) {
            this.messagealertvalue('请输入有效值', 'error')
          } else {
            textarea3lastvalue = textarea3lastvalue.replace(/;+/g, ';')
            for (let z = 0; z < groupvaluelist.length; z++) {
              if ((this.value9).indexOf(groupvaluelist[z]) === -1) {
                let groupvalemessageone = await axios.get(this.serviceurl() + '/api/GetGroupPreMessage/?CountName=' + groupvaluelist[z])
                if (groupvalemessageone.data.isSuccess) {
                  this.value9.push(groupvaluelist[z])
                  textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
                }
              } else {
                textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
              }
            }
            this.textarea3 = textarea3lastvalue
            if (textarea3lastvalue === '') {
              this.messagealertvalue('成员搜索完毕', 'success')
            } else {
              this.messagealertvalue('部分成员搜索失败，请核实', 'warning')
            }
          }
        }
      }
    },
    dataBackFillGoods (row) {
      if ((event.target.tagName).toString() !== 'SPAN') {
        let winWidth = 0
        let winHeight = 0
        let winHeightlastvalue = ''
        let winWidthlastvalue = ''
        if (window.innerWidth) {
          winWidth = window.innerWidth
        } else if ((document.body) && (document.body.clientWidth)) {
          winWidth = document.body.clientWidth
        }
        if (window.innerHeight) {
          winHeight = window.innerHeight
        } else if ((document.body) && (document.body.clientHeight)) {
          winHeight = document.body.clientHeight
        }
        if (Math.ceil(winHeight * 0.8) <= 694) {
          winHeightlastvalue = (694).toString()
        } else {
          winHeightlastvalue = Math.ceil(winHeight * 0.8).toString()
        }
        if (Math.ceil(winWidth * 0.5) <= 985) {
          winWidthlastvalue = (985).toString()
        } else {
          winWidthlastvalue = Math.ceil(winWidth * 0.5).toString()
        }
        var hrefurlspace = 'height=' + winHeightlastvalue + ',width=' + winWidthlastvalue
        // window.open('http://' + window.location.host + '/' + row.typevalueall + '/?disName=' + row.samname, '_blank', hrefurlspace)
        window.open('http://' + window.location.host + '/intermediate/?objectDN=' + encodeURIComponent(row.samname), '_blank', hrefurlspace)
      }
    },
    async findgroupmembers () {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      let memberslist = []
      await axios
        .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.sAMAccountName = response.data.message.sAMAccountName
            memberslist = response.data.message.memberOf
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('加载失败', 'error')
            }
          }
          // this.tableData = [{name: response.data.message.userPrincipalName}]
        })
        .catch(function () {
          this.messagealertvalue('加载失败', 'error')
        })
      for (let i = 0; i < memberslist.length; i++) {
        // let sAMAccountNamevalue = ''
        // let typevalue = ''
        // var responsevalue = await axios.get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + memberslist[i] + '&objectClass=DN')
        // if (responsevalue.data.isSuccess) {
        //   if ((responsevalue.data.message.objectClass).indexOf('group') > -1) {
        //     sAMAccountNamevalue = responsevalue.data.message.sAMAccountName
        //     typevalue = 'groupvalue'
        //   } else if ((responsevalue.data.message.objectClass).indexOf('person') > -1 && (responsevalue.data.message.objectClass).indexOf('user') > -1) {
        //     sAMAccountNamevalue = responsevalue.data.message.sAMAccountName
        //     typevalue = 'searchuser'
        //   } else {
        //     this.messagealertvalue('信息获取失败', 'error')
        //   }
        // } else {
        //   if (responsevalue.data.message === '权限不足') {
        //     this.messagealertvalue('权限不足', 'error')
        //   } else {
        //     this.messagealertvalue('信息获取失败', 'error')
        //   }
        // }
        this.tableData3.push({name: ((memberslist[i]).split('CN=')[1]).split(',')[0], date: memberslist[i], samname: memberslist[i], typevalueall: memberslist[i]})
      }
    },
    addGroup () {
      this.dialogVisible = true // 模态框是否显示
      this.options4 = []
      this.value9 = []
      this.textarea3 = null
      this.loading = false
    },
    remoteMethod (query) {
      if (query !== '') {
        this.loading = true
        axios
          .get(this.serviceurl() + '/api/GetGroupAnrMessage/?CountName=' + query)
          .then(response => {
            this.options4 = response.data.message
            this.loading = false
          })
      } else {
        this.options4 = []
      }
    },
    addgrouptrue () {
      let GdisNameList = ''
      for (let i = 0; i < (this.value9).length; i++) {
        GdisNameList = GdisNameList + '&GdisNameList=' + (this.value9)[i]
      }
      axios
        .get(this.serviceurl() + '/api/AddUserToGroup/?CountName=' + this.sAMAccountName + GdisNameList)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('添加成功', 'success')
            this.dialogVisible = false
            this.tableData3 = []
            this.findgroupmembers()
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('添加失败', 'error')
            }
          }
        })
        .catch(function () {
          this.messagealertvalue('添加失败', 'error')
        })
    },
    Deletegroup (index, row) {
      this.$confirm('此操作将退出' + row.name + '群组, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/DelGroupUser/?GdisName=' + row.date + '&CountName=' + this.sAMAccountName)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  (this.tableData3).splice(index, 1)
                  this.messagealertvalue('群组退出成功', 'success')
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('群组退出失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then()
    },
    Deleteallgroup () {
      this.$confirm('此操作将退出所有群组, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/EmUserGroup/?CountName=' + this.sAMAccountName)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.tableData3 = []
                  this.findgroupmembers()
                  this.messagealertvalue('群组退出成功', 'success')
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('群组退出失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then()
    }
  }
}
</script>
<style>
</style>
