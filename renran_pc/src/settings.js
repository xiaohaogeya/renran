export default {
  Host:"http://api.renran.cn:8000",
  TC_captcha:{
    app_id: "2072894469",
  },

  save_user(storage, data){
    if(storage === sessionStorage){
      var Storage = localStorage;
    }else{
      var Storage = sessionStorage;
    };

    Storage.removeItem("user_token");
    Storage.removeItem("user_name");
    Storage.removeItem("user_id");
    Storage.removeItem("user_nickname");
    Storage.removeItem("user_avatar");

    storage.user_token = data.token;
    storage.user_name = data.username;
    storage.user_id = data.id;
    storage.user_nickname = data.nickname;
    storage.user_avatar = data.avatar;
  },
  jump_page(vm,nickname, title="登陆成功",confirm_text="个人中心",confirm_url="/user", cancel_text="返回上一页"){
    vm.$confirm(`${nickname},欢迎回到荏苒~`, title, {
      confirmButtonText: confirm_text,
      cancelButtonText: cancel_text,
      type: 'success'
    }).then(() => {
      // 跳转到个人中心
      vm.$router.push(confirm_url);
    }).catch(() => {
      // 跳转到上一页
      vm.$router.back();
    });
  },
  check_user_login(vm){
    // 判断用户是否已经登录
    let token = localStorage.user_token || sessionStorage.user_token;
    if(!token){
      // 跳转到登录页面
      this.jump_page(vm, "尊敬的游客,您尚未登录!请登录后再进行操作!", "警告", "去登录", "/user/login");
    }
    return token;
  }

}

