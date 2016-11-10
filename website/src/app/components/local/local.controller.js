import $ from 'jquery';

class LocalController {
  constructor($scope) {
    "ngInject";
    this.name = 'local';
    this.$scope = $scope;
  }

  $onInit(){
    this.appendTo = document.querySelector('.images');
    this.name = 'imagelist';
    this.data = [];

    $.ajax({
      type: "GET",
      url: "http://10.1.4.173:8000/api/images",
      success: res => {
        let results = res;

        results.map(result => {
          result.created_at = result.created_at.split('T')[0];
          const verified = result.blockchain_verified;
          if (verified) {
            result.blockchain_verified = "可信";
          } else {
            result.blockchain_verified = "不可信";
          }
          this.$scope.$apply(() => {
            this.data.push(result);
          });
        }); 
      }
    });
  }
}

export default LocalController;
