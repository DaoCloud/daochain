import template from './person.html';
import $ from 'jquery';
// import controller from './person.controller';
import './person.scss';
import Web3 from 'web3';

function Inject(...dependencies) {
    return function decorator(target, key, descriptor) {
        if (descriptor) {
            const fn = descriptor.value;
            fn.$inject = dependencies;
        } else {
            target.$inject = dependencies;
        }
    };
}
@Inject('$scope', '$state', '$http', 'appConfig', '$interval')
class PersonController {
    constructor($scope, $state, $http, appConfig, $interval) {
        "ngInject";
        this.name = 'person';
        this.scope = $scope;
        this.$state = $state;
        this.$http = $http;
        this.$interval = $interval;
        this.APIUrl = appConfig.APIUrl;
        this.LocalUrl = appConfig.LocalUrl;
        this.Web3Url = appConfig.Web3Url;
        this.userInfo = {
            username: localStorage.getItem('username'),
            avatar: localStorage.getItem('user-avatar')
        }
        this.username = localStorage.getItem('username');
        this.tabIndex = 0;
        this.titleName = '组织信息';
        this.walletAddress = '';
        this.web3 = new Web3(new Web3.providers.HttpProvider(this.Web3Url));
        this.isMining = this.web3.eth.mining;
        this.hashrate = this.web3.eth.hashrate / 1000;
        this.monitBalance = () => {
            this.moniter = this.$interval(() => {
                this.defaultAddress = this.web3.eth.getBalance(this.web3.eth.coinbase);
                this.balance = this.web3.fromWei(this.defaultAddress, 'ether').toNumber();
                this.hashrate = this.web3.eth.hashrate / 1000;
            }, 4000);
        }

        this.changeMine = () => {
//            console.log(this.web3);
            let requestDataStart = {
                "jsonrpc": "2.0",
                "method": "miner_start",
                "params": [1],
                "id": 74
            };
            let requestDataStop = {
                "jsonrpc": "2.0",
                "method": "miner_stop",
                "params": [],
                "id": 74
            };
            if (this.isMining) {
                this.monitBalance();
                this.$http({
                    method: "POST",
                    url: this.Web3Url,
                    headers: {
                        "Content-Type": "application/json"
                    },
                    data: JSON.stringify(requestDataStart)
                }).then(res => {
//                    console.log(res);
                });
            } else {
                this.$interval.cancel(this.moniter);
                this.$http({
                    method: "POST",
                    url: this.Web3Url,
                    headers: {
                        "Content-Type": "application/json"
                    },
                    data: JSON.stringify(requestDataStop)
                }).then(res => {
                    console.log(res);
                });
            }
        }

        this.logout = () => {
            localStorage.clear();
            this.$state.go('home');
        }
    }

    $onInit() {
        (() => {
            let localList = this.web3.personal.listAccounts;
            if (localList) {
                this.defaultAddress = this.web3.eth.getBalance(this.web3.eth.coinbase);
                this.balance = this.web3.fromWei(this.defaultAddress, 'ether').toNumber();
            }
            this.walletAddress = localList[0];

            if (this.isMining) {
                this.monitBalance();
            }
        })();
    }
}

let personComponent = {
    restrict: 'E',
    bindings: {},
    template,
    controller: PersonController
};

export default personComponent;
