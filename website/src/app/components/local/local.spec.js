import LocalModule from './local'
import LocalController from './local.controller';
import LocalComponent from './local.component';
import LocalTemplate from './local.html';

describe('Local', () => {
  let $rootScope, makeController;

  beforeEach(window.module(LocalModule));
  beforeEach(inject((_$rootScope_) => {
    $rootScope = _$rootScope_;
    makeController = () => {
      return new LocalController();
    };
  }));

  describe('Module', () => {
    // top-level specs: i.e., routes, injection, naming
  });

  describe('Controller', () => {
    // controller specs
    it('has a name property [REMOVE]', () => { // erase if removing this.name from the controller
      let controller = makeController();
      expect(controller).to.have.property('name');
    });
  });

  describe('Template', () => {
    // template specs
    // tip: use regex to ensure correct bindings are used e.g., {{  }}
    it('has name in template [REMOVE]', () => {
      expect(LocalTemplate).to.match(/{{\s?\$ctrl\.name\s?}}/g);
    });
  });

  describe('Component', () => {
      // component/directive specs
      let component = LocalComponent;

      it('includes the intended template',() => {
        expect(component.template).to.equal(LocalTemplate);
      });

      it('invokes the right controller', () => {
        expect(component.controller).to.equal(LocalController);
      });
  });
});
