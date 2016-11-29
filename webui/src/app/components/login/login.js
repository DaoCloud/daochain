import angular from 'angular';
import uiRouter from 'angular-ui-router';
import loginComponent from './login.component';

let loginModule = angular.module('login', [
  uiRouter
])
.config(($stateProvider) => {
  "ngInject";
  $stateProvider
    .state('login', {
      url: '/login',
      component: 'login',
      onEnter: ($state) => {
	        "ngInject";
	     	localStorage.clear();
	    }
    });
})
.component('login', loginComponent)
.name;

export default loginModule;
