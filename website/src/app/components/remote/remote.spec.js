import MarketModule from './remote'
import MarketController from './remote.controller';
import MarketComponent from './remote.component';
import MarketTemplate from './remote.html';

describe('Market', () => {
  let $rootScope, makeController;

  beforeEach(window.module(MarketModule));
  beforeEach(inject((_$rootScope_) => {
    $rootScope = _$rootScope_;
    makeController = () => {
      return new MarketController();
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
      expect(MarketTemplate).to.match(/{{\s?\$ctrl\.name\s?}}/g);
    });
  });

  describe('Component', () => {
      // component/directive specs
      let component = MarketComponent;

      it('includes the intended template',() => {
        expect(component.template).to.equal(MarketTemplate);
      });

      it('invokes the right controller', () => {
        expect(component.controller).to.equal(MarketController);
      });
  });
});
