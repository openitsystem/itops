<template>
  <div id="app1">
  </div>
</template>
<script>
import axios from 'axios'
import serverurlvaluefromjs from '@/config/serverurlvalue'
axios.defaults.withCredentials = true
export default {
  async created () {
    let disNameforurl = this.getQueryVariable('disName')
    if (!disNameforurl) {
      let objectDNforurl = this.getQueryVariabledecode('objectDN')
      await this.getsamaccountvaluebydn(objectDNforurl)
    }
  },
  methods: {
    async getsamaccountvaluebydn (objectDNforurl) {
      let responsevalue = await axios.get(serverurlvaluefromjs.serverurl + '/api/GetUserMessage/?CountName=' + objectDNforurl + '&objectClass=DN')
      let sAMAccountNamevalue = ''
      let typevalue = ''
      if (responsevalue.data.isSuccess) {
        if ((responsevalue.data.message.objectClass).indexOf('group') > -1) {
            sAMAccountNamevalue = responsevalue.data.message.sAMAccountName
            typevalue = 'groupvalue'
            window.location.href = 'http://' + window.location.host + '/' + typevalue + '?disName=' + sAMAccountNamevalue
          } else if ((responsevalue.data.message.objectClass).indexOf('computer') > -1) {
            sAMAccountNamevalue = responsevalue.data.message.sAMAccountName
            typevalue = 'computervalue'
            window.location.href = 'http://' + window.location.host + '/' + typevalue + '?disName=' + sAMAccountNamevalue
          } else if ((responsevalue.data.message.objectClass).indexOf('contact') > -1) {
            sAMAccountNamevalue = encodeURIComponent(responsevalue.data.message.distinguishedName)
            typevalue = 'contactvalue'
            window.location.href = 'http://' + window.location.host + '/' + typevalue + '?disName=' + sAMAccountNamevalue
          } else if ((responsevalue.data.message.objectClass).indexOf('person') > -1 && (responsevalue.data.message.objectClass).indexOf('user') > -1) {
            sAMAccountNamevalue = responsevalue.data.message.sAMAccountName
            typevalue = 'searchuser'
            window.location.href = 'http://' + window.location.host + '/' + typevalue + '?disName=' + sAMAccountNamevalue
          }
      }
    },
    getQueryVariable: function (variable) {
      let query = window.location.search.substring(1)
      let vars = query.split('&')
      for (let i = 0; i < vars.length; i++) {
        let pair = vars[i].split('=')
        if (pair[0] === variable) {
          return decodeURI(pair[1])
        }
      }
      return (false)
    },
    getQueryVariabledecode: function (variable) {
      let query = window.location.search.substring(1)
      let vars = query.split('&')
      for (let i = 0; i < vars.length; i++) {
        let pair = vars[i].split('=')
        if (pair[0] === variable) {
          return decodeURIComponent(pair[1])
        }
      }
      return (false)
    }
  }
}
</script>

