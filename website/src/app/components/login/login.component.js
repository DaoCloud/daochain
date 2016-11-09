import template from './login.template.html';
import controller from './login.controller.js';
import './login.scss';

let loginComponent = {
  restrict: 'E',
  bindings: {},
  template,
  controller,
  controllerAs: 'vm',
  bindToController: true
};

export default loginComponent;
