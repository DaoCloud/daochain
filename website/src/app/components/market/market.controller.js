import $ from 'jquery';

class MarketController {
    constructor($scope, appConfig, $state, $http) {
        "ngInject";
        this.name = 'market';
        this.$scope = $scope;
        this.$http = $http;
        this.$state = $state;
        this.searchImage = '';
        this.pageNumber = 1;
        this.pageSize = 5;
        this.APIUrl = appConfig.APIUrl;
        this.localUrl = appConfig.LocalUrl;
    }

    $onInit() {
        this.appendTo = document.querySelector('.images');
        this.name = 'imagelist';
        this.data = [];

        this.updateData = (res) => {
            this.data = [];
            let results = res.data.results;
            this.nowPageNumber = res.data.page;
            this.totalPageNumber = res.data.total_pages;
            results.map(result => {
                result.created_at = result.created_at.split('T')[0];
                result.updated_at = result.updated_at.split('T')[0];
                const verified = result.blockchain_verified;
                if (verified) {
                    result.blockchain_verified = "可信";
                } else {
                    result.blockchain_verified = "不可信";
                }
                this.data.push(result);
            });
        }

        this.search = () => {
            this.$http({
                method: 'GET',
                url: `http://api.daocloud.co/hub/v2/blockchain/verified-public-repos?q=${this.searchImage}&page=${this.pageNumber}&page_size=${this.pageSize}`,
                headers: {
                    "Authorization": localStorage.getItem('token'),
                }
            }).then(res => {
                this.updateData(res);
            });
        }

        this.getVerifiedRepo = () => {
            this.$http({
                method: 'GET',
                url: `http://api.daocloud.co/hub/v2/blockchain/verified-public-repos?page=${this.pageNumber}&page_size=${this.pageSize}`,
                headers: {
                    "Authorization": localStorage.getItem('token'),
                }
            }).then(res => {
                this.updateData(res);
            });
        }

        this.lastPage = () => {
            this.pageNumber--;
            this.getVerifiedRepo();
        }

        this.nextPage = () => {
            this.pageNumber++;
            this.getVerifiedRepo();
        }

        this.getVerifiedRepo();
    }
}

export default MarketController;
