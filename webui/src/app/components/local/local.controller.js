import $ from 'jquery';
import Web3 from 'web3';
import dialogTemplate from './dialog.html';
// import AppConfig from '../../app.config.js';

class DialogController {
    constructor($scope, $http, appConfig, image) {
        "ngInject";
        this.$scope = $scope;
        this.$http = $http;
        this.pwd = "";
        this.errorMessage = "";
        this.error = false;
        this.image = image;
        this.localUrl = appConfig.LocalUrl;
        this.Web3Url = appConfig.Web3Url;
        this.web3 = new Web3(new Web3.providers.HttpProvider(this.Web3Url));

        this.checkPwd = () => {
            try {
                let couldUnlock = this.web3.personal.unlockAccount(this.web3.eth.coinbase, this.pwd, 5000);
                if (couldUnlock) {
                    this.$close();
                    this.signImage(this.image);
                }
            } catch (e) {
                this.errorMessage = e.message;
                this.error = true;
            }
        }
    }
}

class LocalController {
    constructor($scope, appConfig, $daoDialog, $http, $state, $interval, $timeout) {
        "ngInject";
        this.name = 'local';
        this.$scope = $scope;
        this.$daoDialog = $daoDialog;
        this.$http = $http;
        this.$state = $state;
        this.$interval = $interval;
        this.$timeout = $timeout;
        this.defaultNameSpace = localStorage.getItem('username');
        this.localUrl = appConfig.LocalUrl;
        this.APIUrl = appConfig.APIUrl;
        this.Web3Url = appConfig.Web3Url;
        this.web3 = new Web3(new Web3.providers.HttpProvider(this.Web3Url));
    }

    $onInit() {
        this.appendTo = document.querySelector('.images');
        let accounts = this.web3.eth.accounts;
        if (!accounts.length) {
            this.$state.go('person');
        }
        this.name = 'imagelist';
        this.data = [];
        this.verifyImage = (tag) => {
            const postData = {
                "repo_tag": this.data[tag].repo_tag
            };

            // $.ajax({
            //     type: "POST",
            //     url: this.localUrl + "/verify-image",
            //     data: JSON.stringify(postData),
            //     headers: {
            //         "Content-Type": "application/json"
            //     },
            //     success: res => {
            //         const verify = res.verify;
            //         const signed = res.signed;
            //         this.$scope.$apply(() => {
            //             this.data[tag].show = false;
            //             if (!signed) {
            //                 this.data[tag].blockchain_verified = "未签名";
            //                 this.data[tag].text_color = "grey";
            //                 this.data[tag].can_sign = true;
            //             } else if (!verify) {
            //                 this.data[tag].blockchain_verified = "验证失败";
            //                 this.data[tag].text_color = "red";
            //                 this.data[tag].can_sign = false;
            //             } else {
            //                 this.data[tag].blockchain_verified = "已验证";
            //                 this.data[tag].text_color = "green";
            //                 this.data[tag].can_sign = false;
            //             }
            //         });
            //     }
            // });

            this.$http({
                method: "POST",
                url: `${this.localUrl}/verify-image`,
                data: JSON.stringify(postData),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(res => {
                const verify = res.data.verify;
                const signed = res.data.signed;
                this.data[tag].show = false;
                if (!signed) {
                    this.data[tag].blockchain_verified = "未签名";
                    this.data[tag].text_color = "grey";
                    this.data[tag].can_sign = true;
                } else if (!verify) {
                    this.data[tag].blockchain_verified = "验证失败";
                    this.data[tag].text_color = "red";
                    this.data[tag].can_sign = false;
                } else {
                    this.data[tag].blockchain_verified = "已验证";
                    this.data[tag].text_color = "green";
                    this.data[tag].can_sign = false;
                }
            }, err => {
                // console.log(err);
                // tenant_not_found
                if (err.status === 404 && err.data.error_id === 'tenant_not_found') {
                    this.data[tag].show = false;
                    this.data[tag].blockchain_verified = "未签名";
                    this.data[tag].text_color = "grey";
                    this.data[tag].can_sign = true;
                }
            });
        }

        this.openDialog = (obj) => {
            const dialog = this.$daoDialog.open({
                template: dialogTemplate,
                controller: DialogController,
                controllerAs: "vm",
                bindToController: true,
                scope: this.$ctrl,
                resolve: {
                    image: () => obj,
                }
            });

            dialog.result.then(() => {
                const signImage = ({ tag, id, $index }) => {
                    this.data[$index].is_sign = true;
                    this.data[$index].blockchain_verified = "正在计算Hash";

                    const postData = {
                        "image_id": id,
                        "repo_tag": tag
                    }

                    const getCheckedBlockNumber = (baseNumber) => {
                        let getNumber = this.$interval(() => {
                            let res = parseInt(this.web3.eth.blockNumber, 16);
                            this.data[$index].writtenBlocks = res - parseInt(baseNumber, 16) + 1;
                            if (this.data[$index].writtenBlocks >= 2) {
                                this.data[$index].blockchain_verified = "已验证";
                                this.data[$index].text_color = "green";
                            }
                        }, 1000);
                    }

                    const has_signed = (tx) => {
                        let getBlockNumber = this.$interval(() => {
                            const web3 = new Web3(new Web3.providers.HttpProvider("http://10.1.4.173:8545"));
                            let res = web3.eth.getTransaction(tx);
                            if (res.blockNumber) {
                                this.$interval.cancel(getBlockNumber);
                                this.data[$index].writtenBlocks++;
                                getCheckedBlockNumber(res.blockNumber);
                            }
                        }, 3000);
                    }

                    const startSign = () => {
                        let startSignProgess = this.$interval(() => {
                            if (this.data[$index].sign_val > 0.95) {
                                this.$http.cancel(startProgess);
                            }
                            let random_increment = 0.1 / this.hash_time;
                            this.data[$index].sign_val += random_increment;
                        }, 100);

                        this.$http({
                            method: "POST",
                            url: this.localUrl + "/sign-image",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            data: JSON.stringify(postData)
                        }).then(res => {
                            this.data[$index].blockchain_verified = "正在写入区块链";
                            this.data[$index].is_sign = false;
                            this.$interval.cancel(startSignProgess);
                            this.data[$index].writeIntoBlockChain = true;
                            has_signed(res.data.tx);
                        }, err => {
                            this.data[$index].is_sign = false;
                            if (err.data.msg === 'not enough balance') {
                                this.data[$index].blockchain_verified = "余额不足，请去[个人设置]页面开始挖矿";
                                this.data[$index].text_color = "orange";
                            } else {
                                this.data[$index].blockchain_verified = "未知错误，请尝试重新签名";
                                this.data[$index].text_color = "orange";
                            }
                        });
                    }

                    this.$http({
                        method: "GET",
                        url: `${this.localUrl}/hash-estimate`,
                        params: {
                            'repo_tag': tag
                        }
                    }).then(res => {
                        this.hash_time = res.data;
                        startSign();
                    });
                }
                signImage(obj);
            });

        }

        this.startSignRepo = (tag, id, $index) => {
            this.openDialog({ tag, id, $index });
        }
        this.$http({
            method: "GET",
            url: `${this.localUrl}/images`,
        }).then(res => {
            let results = res.data;
            let rid = 0;
            results.map(result => {
                result.created_at = result.created_at.split('T')[0];
                const verified = result.blockchain_verified;
                if (verified) {
                    result.blockchain_verified = "可信";
                } else {
                    result.blockchain_verified = "不可信";
                }
                result.show = true;
                result.is_sign = false;
                result.sign_val = 0;
                result.disableSetter = (result.registry == 'daocloud.io' && result.namespace == this.defaultNameSpace) ? false : true;
                result.writeIntoBlockChain = false;
                result.writtenBlocks = 0;
                this.data.push(result);
                this.verifyImage(rid);
                rid++;
            });
        });
    }
}

export default LocalController;