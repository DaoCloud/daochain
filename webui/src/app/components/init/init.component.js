import template from './init.html';
import $ from 'jquery';
import Web3 from 'web3';
import './init.scss';

class controller {
    constructor($scope, appConfig, $http, $state) {
        "ngInject";
        this.$scope = $scope;
        this.$http = $http;
        this.$state = $state;
        this.APIUrl = appConfig.APIUrl;
        this.localUrl = appConfig.LocalUrl;
        this.Web3Url = appConfig.Web3Url;
        this.nestedStepIndex = 1;
        this.orgList = [];
        this.selectedOrg = "";
        this.walletSet = true;
        this.pwd = "";
        this.errInfo = "";
        this.walletAccount = "";
        this.web3 = new Web3(new Web3.providers.HttpProvider(this.Web3Url));
        this.createWallet = () => {
            if (this.pwd) {
                try {
                    const new_account = this.web3.personal.newAccount(this.pwd);
                    this.walletAccount = new_account;
                    this.walletSet = false;
                } catch (error) {
                    this.errInfo = error;
                }
            } else {
                this.errInfo = "请输入密码";
            }
        }
        this.finish = () => {
            this.$state.go('remote');
        }
    }

    $onInit() {
        (() => {
            this.$http({
                method: 'GET',
                url: this.APIUrl + '/get-token-info',
                headers: {
                    'Authorization': localStorage.getItem('token')
                }
            }).then((res, status) => {
                res.data.user.tenants.map((tenant) => {
                    if (tenant.active && tenant.is_org) {
                        this.orgList.push(tenant.org_name);
                    }
                });
            });
        })();
    }
}

const initComponent = {
    restrict: 'E',
    bindings: {},
    template,
    controller,
};

export default initComponent;