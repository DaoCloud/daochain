import angular from 'angular';
import uiRouter from 'angular-ui-router';
import loginComponent from '../../components/login/login.component.js';

let loginModule = angular.module('login', [
  uiRouter
])

.config(($stateProvider) => {
  "ngInject";

  $stateProvider
    .state('login', {
      url: '/login',
      component: 'login',
    });
})

.component('login', loginComponent)

.name;

export default loginModule;
