import angular from 'angular';
import uiRouter from 'angular-ui-router';
import remoteComponent from './remote.component';

let remoteModule = angular.module('remote', [
        uiRouter
    ])
    .config(($stateProvider, $locationProvider) => {
        "ngInject";
        $locationProvider.html5Mode(true);
        $stateProvider
            .state('remote', {
                url: '/',
                data: {
                    requireAuth: true
                },
                component: 'remote'
            });
    })
    .component('remote', remoteComponent)
    .name;

export default remoteModule;
