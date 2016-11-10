import template from './person.html';
import $ from 'jquery';
// import controller from './person.controller';
import './person.scss';
import Web3 from 'web3';

const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
let balance = web3.fromWei(web3.eth.getBalance("0xfb23180d733d3e40463b7e14745173b10e179f2e"), 'ether');

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
class PersonController {
  constructor($scope) {
    this.name = 'person';
    this.scope = $scope;
    this.isMining = web3.eth.mining;
    this.balance = balance.toNumber();
    this.walletList = [];
    this.deleteWallet = function (content, index) {
      this.walletList.splice(index, 1);
      $.ajax({
        type: "DELETE",
        url: "http://api.daocloud.co/hub/v2/blockchain/addresses/"+ content,
        headers: {
          "Authorization": "ImU5NjYwMzUxLTMyY2UtNGE2OS05MGRiLTA2YzNlMGVjNzE1MSI.CwNVBg.FFx7wUGgflqynUsMktEjWcdC_cg"
        },
        success: (res) => {
          console.log(res);
        }
      });
    }

    this.newWallet = function () {
      $('.wallet > .add-new').css('display', 'block');
    }

    this.getWalletValue = function () {
      // console.log($('.wallet > .add-new > input'));
      $('.dao-input-container.icon-inside').attr('loading', 'true');
      const str = $('.wallet > .add-new input')[0].value;
      const new_account = web3.personal.newAccount(str);
      $('.wallet > .add-new').css('display', 'none');
      let sentData = {
        "address": new_account
      };
      $.ajax({
        type: "POST",
        url: " http://api.daocloud.co/hub/v2/blockchain/addresses",
        headers: {
          "Authorization": "ImU5NjYwMzUxLTMyY2UtNGE2OS05MGRiLTA2YzNlMGVjNzE1MSI.CwNVBg.FFx7wUGgflqynUsMktEjWcdC_cg",
          "Content-Type": "application/json"
        },
        data: JSON.stringify(sentData),
        success: (res) => {
          this.scope.$apply(() => {
            this.walletList.push(res.address);
          });
        }
      });
    }

    this.changeMine = () => {
      console.log(web3);
      let requestDataStart = {
        "jsonrpc": "2.0",
        "method": "miner_start",
        "params": [],
        "id": 74
      };
      let requestDataStop = {
        "jsonrpc": "2.0",
        "method": "miner_stop",
        "params": [],
        "id": 74
      };
      if (this.isMining) {
        // web3.miner.start();
        $.ajax({
          type: "POST",
          url: "http://localhost:8545",
          headers: {
            "Content-Type": "application/json"
          },
          data: JSON.stringify(requestDataStart),
          success: (res) => {
            console.log(res);
          }
        });
      } else {
        $.ajax({
          type: "POST",
          url: "http://localhost:8545",
          headers: {
            "Content-Type": "application/json"
          },
          data: JSON.stringify(requestDataStop),
          success: (res) => {
            console.log(res);
          }
        });
      }
    }
  }

  $onInit() {
    (()=>{
      $.ajax({
        type: "GET",
        url: "http://api.daocloud.co/hub/v2/blockchain/addresses",
        headers: {
          "Authorization": "ImU5NjYwMzUxLTMyY2UtNGE2OS05MGRiLTA2YzNlMGVjNzE1MSI.CwNVBg.FFx7wUGgflqynUsMktEjWcdC_cg"
        },
        success: (res) => {
          const results = res.results;
          this.scope.$apply(() => {
            results.forEach(v => {
              this.walletList.push(v.address);
            })
          });
        }
      });
    })();
  }
}

let personComponent = {
  restrict: 'E' ,
  bindings: {},
  template,
  controller: PersonController
};

export default personComponent;
