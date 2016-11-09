import angular from 'angular';
import uiRouter from 'angular-ui-router';
import remoteComponent from './remote.component';

let remoteModule = angular.module('remote', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('remote', {
			url: '/remote',
			component: 'remote'
		});
})
.component('remote', remoteComponent)
  .name;

export default remoteModule;
