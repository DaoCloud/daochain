import angular from 'angular';
import uiRouter from 'angular-ui-router';
import localComponent from './local.component';

let localModule = angular.module('local', [
  uiRouter
])
.config(($stateProvider, $locationProvider) => {
	"ngInject";
	$stateProvider
		.state('local', {
			url: '/local',
      data: {
        requireAuth: true
      },
			component: 'local'
		});
    // $locationProvider.html5Mode(false);
})
.component('local', localComponent)
  .name;

export default localModule;
