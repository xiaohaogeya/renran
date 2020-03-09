<template>

</template>

<script>
    export default {
        name: "QQCallBack",
        created() {

        },
        methods:{
          get_user_info(){
            // 转发code提供给服务端
            this.$axios.get(`${this.$settings.Host}/oauth/qq/info/` + location.search
            ).then(response=>{
              console.log("暂作处理");
            }).catch(error=>{
              this.$message.error("网络错误,无法使用QQ登录")
            })
          }
        }
    }
</script>

<style scoped>

</style>
