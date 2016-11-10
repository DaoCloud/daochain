import angular from 'angular';
import uiRouter from 'angular-ui-router';
import personComponent from './person.component';

let personModule = angular.module('person', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('person', {
			url: '/person',
      data: {
        requireAuth: true
      },
			component: 'person'
		});
})
.component('person', personComponent)
  .name;

export default personModule;
