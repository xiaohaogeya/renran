import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import QQCallBack from "../components/QQCallBack";
Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/',
      name: "Home",
      component: Home,
    },
    {
      path: "/home",
      name: "Home",
      component: Home,
    },
    {
      name: "Login",
      path: "/user/login",
      component: Login
    },
    {
      name: "Register",
      path: "/user/register",
      component: Register
    },
    {
      name: "QQCallBack",
      // 改成自己注册QQ登录时的地址,不是一定要.html
      path: "/oauth_callback.html",
      component: QQCallBack
    },
  ]
})
