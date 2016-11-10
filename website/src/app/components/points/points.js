import angular from 'angular';
import uiRouter from 'angular-ui-router';
import pointsComponent from './points.component';

let pointsModule = angular.module('points', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('points', {
			url: '/points',
      data: {
        requireAuth: true
      },
			component: 'points'
		});
})
.component('points', pointsComponent)
  .name;

export default pointsModule;
