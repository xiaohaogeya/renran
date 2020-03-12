// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"
import ElementUI from "element-ui"
import "element-ui/lib/theme-chalk/index.css"
import "../static/css/reset.css"
import "../static/css/iconfont.css"
import "../static/css/iconfont.eot"
import "../static/js/TCaptcha"
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import axios from 'axios'
axios.defaults.withCredentials = false;
Vue.prototype.$axios = axios;
Vue.config.productionTip = false;
Vue.prototype.$settings = settings;
Vue.use(ElementUI);
Vue.use(mavonEditor);
// /* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
