class PersonController {
  constructor() {
    this.name = 'person';
    this.walletList = [
      'aaaaaaaaaaaaaaaaaaaaaaa',
      'bbbbbbbbbbbbbbbbbbbbbbb',
      'ccccccccccccccccccccccc',
    ];
    this.deleteWallet = function (index) {
      this.walletList.splice(index, 1);
    }

    this.newWallet = function (str) {
      const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545");
      console.log(web3);
    }
  }
}

export default PersonController;
