import angular from 'angular';
import uiRouter from 'angular-ui-router';
import localComponent from './local.component';

let localModule = angular.module('local', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('local', {
			url: '/local',
			component: 'local'
		});
})
.component('local', localComponent)
  .name;

export default localModule;
