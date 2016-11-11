import * as constant from './constant';

angular.module('app.config', [])
  .constant('appConfig', {
    APIUrl: constant.API_URL, // http://api.daocloud.co/hub/v2
    LocalUrl: constant.LOCAL_URL, //http://10.1.4.173:8000/api
    // DaoAuth: constant.DAO_AUTH,
    // AuthLogOut: constant.AUTH_LOG_OUT,
    // AuthSignUp: constant.AUTH_SIGN_UP,
    // AuthSignIn: constant.AUTH_SIGN_IN,
    // DaocomAppID: constant.WIDGET_ID,
    // RTMUrl: constant.RTM_URL,
    // PricingUrl: constant.PRICING_URL,
  });

export default 'app.config';
