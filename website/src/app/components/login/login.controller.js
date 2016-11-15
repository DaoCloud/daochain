import $ from 'jquery';

class LoginController {
    constructor($state, AuthService, $scope, appConfig, $http) {
        'ngInject';
        this.$state = $state;
        this.AuthService = AuthService;
        this.captcha_id = "";
        this.captcha_url = "";
        this.$scope = $scope;
        this.$http = $http;
        this.name = 'Login';
        this.ApiUrl = appConfig.APIUrl;
        this.account = {
            "email_or_mobile": "",
            "password": "",
            "captcha_solution": ""
        };

        this.getCapture = () => {
            this.$http({
                method: 'GET',
                url: this.ApiUrl + '/captcha/generate-id',
            }).then((res) => {
                this.captcha_id = res.data.captcha_id;
                this.captcha_url = `${this.ApiUrl}/captcha/image?captcha_id=${res.data.captcha_id}`;
            });
        }
    }

    $onInit() {
        this.getCapture();
    }

    loginGo() {
        $('.errMessage').remove();
        const postData = this.account;
        postData.captcha_id = this.captcha_id;
        this.AuthService.fetchToken(this.account).then(() => {
            this.$state.go('remote');
        });
    }
}

export default LoginController;
