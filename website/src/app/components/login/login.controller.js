class LoginController {
  constructor($state/*, GlobalService, AuthStoreService, AuthService*/) {
    'ngInject';
    this.$state = $state;
    /*
    this.AuthService = AuthService;
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
    // this.GlobalService.login(this.account)
    //   .then((response) => {
    //     const res = response.data;
    //     this.AuthService.setToken(res.token);
    //     this.$state.go('market');
    //   })
  }
}

export default LoginController;
