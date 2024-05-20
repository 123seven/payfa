export default [
  {
    path: '/user',
    layout: false,
    routes: [{name: '登录', path: '/user/login', component: './User/Login'}],
  },
  {path: 'dashboard', name: '仪表盘', icon: 'smile', component: './Dashboard'},
  {
    path: '/admin',
    name: '设置',
    icon: 'crown',
    access: 'canAdmin',
    routes: [
      {path: '/admin', redirect: '/admin/pay-settings'},
      {path: '/admin/pay-settings', name: '支付设置', component: './Manage/PaySetting'},
      {path: '/admin/monitor-settings', name: '监控设置', component: './Manage/MonitorSetting'},
      {path: '/admin/api-settings', name: 'API设置', component: './Manage/ApiSetting'},
    ],
  },
  {name: '订单列表', icon: 'table', path: '/list', component: './TableList'},
  {path: '/', redirect: '/dashboard'},
  {path: '*', layout: false, component: './404'},
];
