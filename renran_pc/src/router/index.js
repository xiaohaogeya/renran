import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import QQCallBack from "../components/QQCallBack";
import Write from "../components/Write";
import PostArticle from "../components/PostArticle";
import Article from "../components/Article";
import Wallet from "../components/Wallet";
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
    {
      name: "Write",
      path: "/writer",
      component: Write
    },
    {
      name: "PostArticle",
      path: "/post",
      component: PostArticle,
    },
    {
      name: "Article",
      path: "/article/:id",
      component: Article,
    },
    {
      name: "Wallet",
      path: "/wallet",
      component: Wallet,
    },

  ]
})
