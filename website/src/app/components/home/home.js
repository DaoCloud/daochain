import angular from 'angular';
import uiRouter from 'angular-ui-router';
import $ from 'jquery';
import 'jquery.cookie';
import homeComponent from './home.component';

let homeModule = angular.module('home', [
  uiRouter
])

.config(($stateProvider, $urlRouterProvider) => {
  "ngInject";

  $urlRouterProvider.otherwise('/');
  // $rootScope.$state = $state;

  $stateProvider
    .state('home', {
      url: '/',
      data: {
        requireAuth: true
      },
      component: 'home',
      onEnter: ($state) => {
        "ngInject";
        if ($.cookie('token')) {

        } else {
          $state.go('login');
        }
      }
    });
})
.component('home', homeComponent)
.name;

export default homeModule;
