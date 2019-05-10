<template>
      <el-menu
        class="el-menu-vertical-demo"
        router
        unique-opened
        @open="handleOpen"
        @close="handleClose">
          <el-menu-item-group class="over-hide" v-for="sub in menu" :key="sub.componentName">
            <el-menu-item :index="sub.componentName" v-text="sub.name" :address.sync="sub.name">
            </el-menu-item>
          </el-menu-item-group>

      </el-menu>
</template>

<style scoped>
  .over-hide{
    overflow: hidden;
  }
  .el-menu-vertical-demo:not(.el-menu--collapse)  {
    height:calc(100vh - 60px)
  }
</style>

<script>
import menu from '@/config/contact-menu-config'
export default {
  data () {
    return {
      menu: menu
    }
  },
  methods: {
    handleOpen (key, keyPath) {
    },
    handleClose (key, keyPath) {
    }
  }
}
</script>
