// import * as constant from './constant';

angular.module('app.config', [])
  .constant('appConfig', {
    APIUrl: "http://api.daocloud.co/hub/v2",
    // DaoAuth: constant.DAO_AUTH,
    // AuthLogOut: constant.AUTH_LOG_OUT,
    // AuthSignUp: constant.AUTH_SIGN_UP,
    // AuthSignIn: constant.AUTH_SIGN_IN,
    // DaocomAppID: constant.WIDGET_ID,
    // RTMUrl: constant.RTM_URL,
    // PricingUrl: constant.PRICING_URL,
  });

export default 'app.config';
