import Web3 from 'web3';

class NavbarController {
  constructor($state, appConfig) {
    "ngInject";
    this.name = 'DaoCloud 区块链验证系统';
    this.$state = $state;
    this.Web3Url = appConfig.Web3Url;
  }

  $onInit() {
  }
}

export default NavbarController;
