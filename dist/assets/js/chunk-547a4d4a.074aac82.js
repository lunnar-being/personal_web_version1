(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-547a4d4a"],{"4ca5":function(e,t,a){"use strict";var n=a("6527"),o=a.n(n);o.a},5669:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n={placeholder:"请选择时间"};t["default"]=n},6527:function(e,t,a){},6604:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t["default"]={today:"今天",now:"此刻",backToToday:"返回今天",ok:"确定",timeSelect:"选择时间",dateSelect:"选择日期",weekSelect:"选择周",clear:"清除",month:"月",year:"年",previousMonth:"上个月 (翻页上键)",nextMonth:"下个月 (翻页下键)",monthSelect:"选择月份",yearSelect:"选择年份",decadeSelect:"选择年代",yearFormat:"YYYY年",dayFormat:"D日",dateFormat:"YYYY年M月D日",dateTimeFormat:"YYYY年M月D日 HH时mm分ss秒",previousYear:"上一年 (Control键加左方向键)",nextYear:"下一年 (Control键加右方向键)",previousDecade:"上一年代",nextDecade:"下一年代",previousCentury:"上一世纪",nextCentury:"下一世纪"}},"677e":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("f6c0"),o=r(n);function r(e){return e&&e.__esModule?e:{default:e}}t["default"]=o["default"]},"882a":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("41b2"),o=u(n),r=a("6604"),i=u(r),s=a("5669"),l=u(s);function u(e){return e&&e.__esModule?e:{default:e}}var c={lang:(0,o["default"])({placeholder:"请选择日期",rangePlaceholder:["开始日期","结束日期"]},i["default"]),timePickerLocale:(0,o["default"])({},l["default"])};c.lang.ok="确 定",t["default"]=c},"9a94":function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("882a"),o=r(n);function r(e){return e&&e.__esModule?e:{default:e}}t["default"]=o["default"]},c4b2:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t["default"]={items_per_page:"条/页",jump_to:"跳至",jump_to_confirm:"确定",page:"页",prev_page:"上一页",next_page:"下一页",prev_5:"向前 5 页",next_5:"向后 5 页",prev_3:"向前 3 页",next_3:"向后 3 页"}},d9ce:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("a-config-provider",{attrs:{locale:e.locale}},[a("div",{staticClass:"index"},[a("a-layout",[a("a-affix",{attrs:{"offset-top":0}},[a("div",{staticClass:"topBar"},[a("div",{staticClass:"flex-spacer"})]),a("div",{staticClass:"header"},[a("div",{staticClass:"headerLogo"},[a("router-link",{attrs:{to:"/store/index"}},[a("span",{staticStyle:{color:"#44ae88"}},[e._v("燕园草木")])])],1),a("div",{staticClass:"tabWrap"},[a("a-menu",{attrs:{mode:"horizontal",selectedKeys:[this.$route.path]}},[a("a-menu-item",{key:"/store/index"},[a("router-link",{attrs:{to:"/store/index"}},[e._v("首页")])],1),a("a-menu-item",{key:"/store/advanced"},[a("router-link",{attrs:{to:"/store/advanced"}},[e._v("高级检索")])],1),a("a-menu-item",{key:"/store/category"},[a("router-link",{attrs:{to:"/store/category"}},[e._v("植物目录浏览")])],1),a("a-menu-item",{key:"/store/features"},[a("router-link",{attrs:{to:"/store/features"}},[e._v("花名和特征检索")])],1),a("a-menu-item",{key:"/store/upload"},[a("router-link",{attrs:{to:"/store/upload"}},[e._v("图像检索")])],1),a("a-menu-item",{key:"/store/map"},[a("router-link",{attrs:{to:"/store/map"}},[e._v("地图")])],1),a("a-menu-item",{key:"/store/contact"},[a("router-link",{attrs:{to:"/store/contact"}},[e._v("联系我们")])],1)],1)],1),a("div",{staticClass:"login-register"},[!1===e.login_status?a("a-button",{staticClass:"login-btn",attrs:{type:"link"},nativeOn:{click:function(t){return t.preventDefault(),e.handleLogin(t)}}},[e._v("登录")]):a("a-button",{staticClass:"login-btn",attrs:{type:"link"},nativeOn:{click:function(t){return t.preventDefault(),e.handleLogout(t)}}},[e._v("登出")]),a("a-button",{staticClass:"register-btn",attrs:{type:"primary"},nativeOn:{click:function(t){return t.preventDefault(),e.handleRegister(t)}}},[e._v("注册")])],1)])]),a("a-layout-content",{staticClass:"content"},[a("app-main")],1),a("a-layout-footer",{staticClass:"footer"},[e._v("\n                版权所有 北京大学信存检小组\n            ")])],1)],1)])},o=[],r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("section",{staticClass:"app-main"},[a("transition",{attrs:{name:"fade",mode:"out-in"}},[a("router-view")],1)],1)},i=[],s={name:"AppMain"},l=s,u=a("2877"),c=Object(u["a"])(l,r,i,!1,null,null,null),d=c.exports,f=a("677e"),p=a.n(f),v={name:"layout2",components:{AppMain:d},data:function(){return{locale:p.a,login_status:!1}},created:function(){this.$store.state.user.token&&(this.login_status=!0)},methods:{handleLogin:function(){this.$router.push({path:"/login"})},handleRegister:function(){this.$router.push({path:"/register"})},handleLogout:function(){this.$store.dispatch("Logout").then(function(){alert("登出成功!")})}},computed:{token:function(){return this.$store.state.user.token}},watch:{token:function(e){this.login_status?this.login_status=!1:this.login_status=!0}}},_=v,m=(a("4ca5"),Object(u["a"])(_,n,o,!1,null,null,null));t["default"]=m.exports},f6c0:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("c4b2"),o=d(n),r=a("882a"),i=d(r),s=a("5669"),l=d(s),u=a("9a94"),c=d(u);function d(e){return e&&e.__esModule?e:{default:e}}t["default"]={locale:"zh-cn",Pagination:o["default"],DatePicker:i["default"],TimePicker:l["default"],Calendar:c["default"],global:{placeholder:"请选择"},Table:{filterTitle:"筛选",filterConfirm:"确定",filterReset:"重置",selectAll:"全选当页",selectInvert:"反选当页",sortTitle:"排序",expand:"展开行",collapse:"关闭行"},Modal:{okText:"确定",cancelText:"取消",justOkText:"知道了"},Popconfirm:{cancelText:"取消",okText:"确定"},Transfer:{searchPlaceholder:"请输入搜索内容",itemUnit:"项",itemsUnit:"项"},Upload:{uploading:"文件上传中",removeFile:"删除文件",uploadError:"上传错误",previewFile:"预览文件",downloadFile:"下载文件"},Empty:{description:"暂无数据"},Icon:{icon:"图标"},Text:{edit:"编辑",copy:"复制",copied:"复制成功",expand:"展开"},PageHeader:{back:"返回"}}}}]);
//# sourceMappingURL=chunk-547a4d4a.074aac82.js.map