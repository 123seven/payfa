import { ProLayoutProps } from '@ant-design/pro-components';

/**
 * @name
 */
const Settings: ProLayoutProps & {
  pwa?: boolean;
  logo?: string;
} = {
  navTheme: 'light',
  colorPrimary: '#F5222D',
  layout: 'top',
  contentWidth: 'Fixed',
  fixedHeader: true,
  fixSiderbar: true,
  colorWeak: false,
  title: 'MiDo',
  pwa: true,
  logo: 'https://gw.alipayobjects.com/zos/bmw-prod/598d14af-4f1c-497d-b579-5ac42cd4dd1f/k7bjua9c_w132_h130.png',
  iconfontUrl: '',
  splitMenus: false,
  footerRender: false,
};

export default Settings;
