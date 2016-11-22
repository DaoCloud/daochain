import angular from 'angular';
import uiRouter from 'angular-ui-router';
import marketComponent from './market.component';

let marketModule = angular.module('market', [
  uiRouter
])
.config(($stateProvider) => {
	"ngInject";
	$stateProvider
		.state('market', {
			url: '/market',
      data: {
        requireAuth: true
      },
			component: 'market'
		});
})
.component('market', marketComponent)
  .name;

export default marketModule;
