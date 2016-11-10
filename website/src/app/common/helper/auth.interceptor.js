/**
 * 用户认证拦截器
 */
function AuthInterceptor($state, $q, appConfig/*, appState*/) {
  'ngInject';

  console.log(appConfig);
  return {
    request(config) {
      if (
        (config.url.indexOf(appConfig.APIUrl) > -1 || config.url.indexOf(appConfig.PricingUrl) > -1)
        && !config.headers.authorization
        && localStorage.getItem('token')) {
        const token = localStorage.getItem('token');
        config.headers.authorization = `Token ${token}`;
      }

      return config;
    },

    responseError(response) {
      if (response.status === 401) {
        AuthStoreService.clean();
        $state.go('login', undefined, { location: true });
      }

      return $q.reject(response);
    },
  };
}

export default AuthInterceptor;
