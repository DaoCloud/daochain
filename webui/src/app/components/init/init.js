import angular from 'angular';
import uiRouter from 'angular-ui-router';
import uiBootstrap from 'angular-ui-bootstrap';
import $ from 'jquery';
import initComponent from './init.component';

let initModule = angular.module('init', [
        uiRouter,
        uiBootstrap
    ])
    .config(($stateProvider, $urlRouterProvider) => {
        "ngInject";
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('init', {
                url: '/init',
                data: {
                    requireAuth: true
                },
                component: 'init'
            });
    })
    .component('init', initComponent)
    .name;

export default initModule;