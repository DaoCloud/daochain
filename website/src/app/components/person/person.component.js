import template from './person.html';
import controller from './person.controller';
import './person.scss';

let personComponent = {
  restrict: 'E' ,
  bindings: {},
  template,
  controller
};

export default personComponent;
