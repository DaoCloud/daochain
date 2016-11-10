import $ from 'jquery';

class LoginController {
  constructor($state, AuthService, $scope) {
    'ngInject';
    this.$state = $state;
    this.AuthService = AuthService;
    this.captcha_id = "";
    this.$scope = $scope;
    this.name = 'Login';
    this.account = {
      "email_or_mobile": "",
      "password": "",
      "captcha_solution": ""
    };

    this.getUserInfo = () => {
      $.ajax({
        type: "GET",
        url: "http://api.daocloud.co/get-token-info",
        headers: {
          "Authorization": localStorage.getItem('token')
        },
        success: res => {
          localStorage.setItem('username', res.user.username);
        }
      });
    }

    this.getCapture = () => {
      $.ajax({
        type: "GET",
        url: "http://api.daocloud.co/captcha/generate-id",
        success: (res) => {
          this.$scope.$apply(() => {
            this.captcha_id = res.captcha_id;
          });
        }
      });
    }
  }

  $onInit () {
    this.getCapture();
  }

  loginGo () {
    $('.errMessage').remove();
    const postData = this.account;
    postData.captcha_id = this.captcha_id;
    console.log(this.account);
    this.AuthService.fetchToken(this.account).then(() =>{
      this.$state.go('home');
      this.getUserInfo();
    });
  }
}

export default LoginController;
