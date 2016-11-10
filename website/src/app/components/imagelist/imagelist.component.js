import template from './imagelist.html';
import $ from 'jquery';
// import controller from './imagelist.controller';
import './imagelist.scss';

function Inject(...dependencies) {
    return function decorator(target, key, descriptor) {
        if(descriptor) {
            const fn = descriptor.value;
            fn.$inject = dependencies;
        } else {
            target.$inject = dependencies;
        }
    };
}

@Inject('$scope')
class controller {
  constructor(scope) {
    // this.dataA = 'sss';
    this.scope = scope;
  }

  $onInit(){
    this.appendTo = document.querySelector('.images');
    this.name = 'imagelist';
    this.data = [];

    $.ajax({
      type: "GET",
      url: "http://api.daocloud.co/hub/v2/hub/daohub/repos?page=1&page_size=10&q=",
      headers: {
        "Authorization": localStorage.getItem('token'),
        "UserNameSpace": ""
      },
      success: res => {
        let results = res.results;
        results.map(result => {
          // console.log(result.created_at);
          result.created_at = result.created_at.split('T')[0];
          result.updated_at = result.updated_at.split('T')[0];
          const verified = result.blockchain_verified;
          if (verified) {
            result.blockchain_verified = "可信";
          } else {
            result.blockchain_verified = "不可信";
          }
          this.scope.$apply(() => {
            this.data.push(result);
          });
        });
      }
    });
  }
}

const imagelistComponent = {
  restrict: 'E',
  bindings: {},
  template,
  controller,
};

export default imagelistComponent;
