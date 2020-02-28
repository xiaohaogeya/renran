import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/common/Login";
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
    }
  ]
})
