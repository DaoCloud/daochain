import angular from 'angular';
import uiRouter from 'angular-ui-router';
import heroComponent from './hero.component';

let heroModule = angular.module('hero', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('hero', {
			url: '/hero',
			component: 'hero'
		});
})
.component('hero', heroComponent)
  .name;

export default heroModule;
