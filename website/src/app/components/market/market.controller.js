import $ from 'jquery';

class MarketController {
    constructor($scope, appConfig) {
        "ngInject";
        this.name = 'market';
        this.$scope = $scope;
        this.APIUrl = appConfig.APIUrl;
        this.localUrl = appConfig.LocalUrl;
    }

    $onInit() {
        this.appendTo = document.querySelector('.images');
        this.name = 'imagelist';
        this.data = [];

        $.ajax({
            type: "GET",
            url: this.APIUrl + "/hub/v2/blockchain/verified-public-repos?page=1&page_size=3",
            headers: {
                "Authorization": localStorage.getItem('token'),
            },
            success: res => {
                let results = res.results;
                results.map(result => {
                    result.created_at = result.created_at.split('T')[0];
                    result.updated_at = result.updated_at.split('T')[0];
                    const verified = result.blockchain_verified;
                    if (verified) {
                        result.blockchain_verified = "可信";
                    } else {
                        result.blockchain_verified = "不可信";
                    }
                    this.$scope.$apply(() => {
                        this.data.push(result);
                    });
                });
            }
        });
    }
}

export default MarketController;