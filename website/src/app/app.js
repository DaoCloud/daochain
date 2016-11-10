import angular from 'angular';
import uiRouter from 'angular-ui-router';
import Common from './common/common';
import Components from './components/components';
import AppComponent from './app.component';
import daoStyle from 'dao-style';
import 'normalize.css';
import { authHookRunBlock } from './routerhooks/require-auth.js';
import AuthService from './common/services/auth.service.js';
import AuthStoreService from './common/services/auth-store.service.js';
import AppConfig from './app.config.js'

angular.module('app', [
    uiRouter,
    daoStyle,
    Common,
    Components,
    AppConfig
  ])
  .config(($locationProvider) => {
    "ngInject";
    // @see: https://github.com/angular-ui/ui-router/wiki/Frequently-Asked-Questions
    // #how-to-configure-your-server-to-work-with-html5mode
    $locationProvider.html5Mode(true).hashPrefix('!');
  })

  .component('app', AppComponent)
  .run(authHookRunBlock)
  .service('AuthService', AuthService)
  .service('AuthStoreService', AuthStoreService);
