import angular from 'angular';
import uiRouter from 'angular-ui-router';
import uiBootstrap from 'angular-ui-bootstrap';
import $ from 'jquery';
import imagelistComponent from './imagelist.component';

let imagelistModule = angular.module('imagelist', [
  uiRouter,
  uiBootstrap
])
.config(($stateProvider, $urlRouterProvider) => {
  "ngInject";
  $urlRouterProvider.otherwise('/');
  $stateProvider
    .state('imagelist', {
      url: '/',
      data: {
        requireAuth: true
      },
      component: 'imagelist'
    });
})
.component('imagelist', imagelistComponent)
.name;

export default imagelistModule;
