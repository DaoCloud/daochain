import $ from 'jquery';

class MarketController {
    constructor($scope, appConfig, $state, $http, $interval, $timeout) {
        "ngInject";
        this.name = 'market';
        this.$scope = $scope;
        this.$http = $http;
        this.$state = $state;
        this.$timeout = $timeout;
        this.$interval = $interval;
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
                result.progress_show = false;
                result.pull_val = 0;
                const verified = result.blockchain_verified;
                if (verified) {
                    result.blockchain_verified = "可信";
                } else {
                    result.blockchain_verified = "不可信";
                }
                this.data.push(result);
            });
        }

        this.runProgress = (index) => {
            // $('.title')[index].style.display = "none";
            this.data[index].progress_show = true;

            let startProgess = this.$interval(() => {
                if (this.data[index].pull_val > 0.8) {
                    this.$interval.cancel(startProgess);
                    console.log("cleare");
                }
                let random_increment = Math.random(1) / 10;
                this.data[index].pull_val += random_increment;
            }, 200);
        }

        this.getPullProgress = (task_id) => {
            this.getProgressInterval = this.$interval(() => {
                this.$http({
                    method: "GET",
                    url: `${this.localUrl}/pull-image`,
                    data: {
                        'task_id': task_id
                    }
                }).then(res => {
                    const percent = res.data.percent;
                    const finished = res.data.finished;
                    if (!finished) {
                        this.pull_val = percent / 100;
                    } else {
                        this.pull_val = 1;
                        this.$interval.cancel(this.getProgressInterval);
                    }
                });
            }, 1000);
        }

        this.pullImage = (image, index) => {
            // debugger;
            const postData = {
                "repo_tag": image
            };

            this.$http({
                method: "POST",
                url: `${this.localUrl}/pull-image`,
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify(postData)
            }).then((res) => {
                const task_id = res.data.task_id;
                this.runProgress(index);
                this.getPullProgress(task_id);

                this.data[index].pull_val = 1;
                this.$timeout(() => {
                    // this.openDialog();
                    this.data[index].progress_show = false;
                }, 100);
            }, err => {
                console.log(err);
            });
        }

        this.search = () => {
            this.$http({
                method: 'GET',
                url: `${this.APIUrl}/hub/v2/blockchain/verified-public-repos?q=${this.searchImage}&page=${this.pageNumber}&page_size=${this.pageSize}`,
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
                url: `${this.APIUrl}/hub/v2/blockchain/verified-public-repos?page=${this.pageNumber}&page_size=${this.pageSize}`,
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