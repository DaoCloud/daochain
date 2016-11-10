class LoginController {
  constructor($state/*, GlobalService, AuthStoreService, */, AuthService) {
    'ngInject';
    this.$state = $state;
    this.AuthService = AuthService;
    /*
    this.AuthStoreService = AuthStoreService;
    this.GlobalService = GlobalService;
    */
    this.name = 'Login';
    this.account = {
      "username": "",
      "password": ""
    };
  }
  loginGo () {
    //this.AuthService.logout();
    console.log(this.account);
    this.AuthService.fetchToken({
      "captcha_id": "Ik5wOVIxRkhlIg.CwXdnw.EaotRPGpsBrf-SUcfJhuXdQubFE",
      "email_or_mobile":"sss",
      "password":"sss",
      "captcha_solution":"2237"
    }).then(() =>{
      this.$state.go('home');
    });

/*
    {
      "captcha_id":"Ik5wOVIxRkhlIg.CwXdnw.EaotRPGpsBrf-SUcfJhuXdQubFE",
      "email_or_mobile":"sss",
      "password":"sss",
      "captcha_solution":"2237"
    }   */
  }
}

export default LoginController;
