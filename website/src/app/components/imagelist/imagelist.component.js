import template from './imagelist.html';
import dialogTemplate from './dialog.html';
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

@Inject('$scope', '$daoDialog')
class controller {
  constructor(scope, $daoDialog) {
    // this.dataA = 'sss';
    this.scope = scope;
    this.$daoDialog = $daoDialog;
  }

  $onInit() {
    this.appendTo = document.querySelector('.images');
    this.name = 'imagelist';
    this.data = [];
    this.val = 0;

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

    this.runProgress = (index) => {
      // $('.title')[index].style.display = "none";
      $('.pull-progress')[index].style.display = "block";

      let startProgess = setInterval(() => {
        if (this.val > 0.8) {
          clearInterval(startProgess);
          console.log("cleare");
        }
        let random_increment = Math.random(1) / 10;
        this.scope.$apply(() => {
          this.val += random_increment;
        });
      }, 200);
    }

    this.pullImage = (image, index) => {
      this.runProgress(index);
      const postData = {
        "repo_tag": image
      };
      $.ajax({
        type: "POST",
        url: "http://10.1.4.173:8000/api/pull-image",
        headers: {
          "Content-Type": "application/json"
        },
        data: JSON.stringify(postData),
        success: res => {
          this.scope.$apply(() => {
            this.val = 1;
          });
          setTimeout(() => {
            this.openDialog();
            $('.pull-progress')[index].style.display = "none";
          }, 100);
        }
      });
    }

    this.openDialog = () => {
      this.$daoDialog.open({
        template: dialogTemplate
      });
    }
  }
}

const imagelistComponent = {
  restrict: 'E',
  bindings: {},
  template,
  controller,
};

export default imagelistComponent;
