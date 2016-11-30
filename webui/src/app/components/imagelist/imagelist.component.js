import template from './imagelist.html';
import dialogTemplate from './dialog.html';
import $ from 'jquery';
// import controller from './imagelist.controller';
import './imagelist.scss';

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
@Inject('$scope', '$daoDialog', 'appConfig', '$http', '$interval', '$timeout')
class controller {
    constructor(scope, $daoDialog, appConfig, $http, $interval, $timeout) {
        // this.dataA = 'sss';
        this.scope = scope;
        this.$http = $http;
        this.$interval = $interval;
        this.$timeout = $timeout;
        this.$daoDialog = $daoDialog;
        this.APIUrl = appConfig.APIUrl;
        this.localUrl = appConfig.LocalUrl;
        this.pageNumber = 1;
        this.searchNumber = 1;
        this.pageSize = 20;
        this.searchImage = '';
    }

    $onInit() {
        this.appendTo = document.querySelector('.images');
        this.name = 'imagelist';
        this.data = [];
        this.val = 0;

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
                    result.blockchain_verified_color = "#22c36a";
                } else {
                    result.blockchain_verified = "不可信";
                    result.blockchain_verified_color = "#f1483f";
                }
                this.data.push(result);
            });
        }

        this.getRemoteRepo = () => {
            this.$http({
                method: 'GET',
                url: `${this.APIUrl}/hub/v2/hub/daohub/repos?page=${this.pageNumber}&page_size=${this.pageSize}`,
                headers: {
                    "Authorization": localStorage.getItem('token'),
                    "UserNameSpace": localStorage.getItem('default-user') !== 'null' && localStorage.getItem('username') ? localStorage.getItem('username') : ""
                }
            }).then(res => {
                this.updateData(res);
            });
        }

        this.getPullProgress = (task_id, index) => {
            this.data[index].progress_show = true;
            this.getProgressInterval = this.$interval(() => {
                // debugger;
                this.$http({
                    method: "GET",
                    url: `${this.localUrl}/pull-image?task_id=${task_id}`
                }).then(res => {
                    if (JSON.stringify(res.data) === '{}') {
                        const percent = res.data.percent;
                        const finished = res.data.finished;
                        if (!finished) {
                            this.data[index].pull_val = percent / 100;
                        } else {
                            this.data[index].pull_val = 1;
                            this.$interval.cancel(this.getProgressInterval);
                            this.data[index].progress_show = false;
                        }
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
                // this.runProgress(index);
                this.getPullProgress(task_id, index);

                // this.data[index].pull_val = 1;
                // this.$timeout(() => {
                //     // this.openDialog();
                //     this.data[index].progress_show = false;
                // }, 100);
            }, err => {
                console.log(err);
            });
        }

        this.search = () => {
            this.$http({
                method: 'GET',
                url: `${this.APIUrl}/hub/v2/hub/daohub/repos?q=${this.searchImage}&page=${this.searchNumber}&page_size=${this.pageSize}`,
                headers: {
                    "Authorization": localStorage.getItem('token'),
                    "UserNameSpace": localStorage.getItem('default-user') !== 'null' && localStorage.getItem('username') ? localStorage.getItem('username') : ""
                }
            }).then(res => {
                this.updateData(res);
            });
        }


        this.openDialog = () => {
            this.$daoDialog.open({
                template: dialogTemplate
            });
        }

        this.lastPage = () => {
            this.pageNumber--;
            this.getRemoteRepo();
        }

        this.nextPage = () => {
            this.pageNumber++;
            this.getRemoteRepo();
        }

        this.getRemoteRepo();
    }
}

const imagelistComponent = {
    restrict: 'E',
    bindings: {},
    template,
    controller,
};

export default imagelistComponent;