import angular from 'angular';
import uiRouter from 'angular-ui-router';
import $ from 'jquery';
import headingComponent from './heading.component';

let headingModule = angular.module('heading', [
  uiRouter
])
.config(($stateProvider) => {
  "ngInject";
  $stateProvider
    .state('heading', {
      url: '/heading',
      component: 'heading'
    });
})
.component('heading', headingComponent)
.name;

export default headingModule;
