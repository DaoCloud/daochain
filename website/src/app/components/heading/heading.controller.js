class HeadingController {
    constructor($timeout, $http, appConfig) {
        "ngInject";
        this.$timeout = $timeout;
        this.$http = $http;
        this.ApiUrl = appConfig.APIUrl;
        this.name = 'heading';
        this.username = localStorage.getItem('username');
    }

    $onInit() {
        this.changeOrg = (tanent) => {
            localStorage.setItem('default-user', tanent.org_name);
            this.username = tanent.org_name;
        }

        (() => {
            this.$http({
                method: 'GET',
                url: this.ApiUrl + '/get-token-info',
                headers: {
                    'Authorization': localStorage.getItem('token')
                }
            }).then((res, status) => {
                this.username = res.data.user.username;
                localStorage.setItem('username', res.data.user.username);
                localStorage.setItem('user-avatar', res.data.user.avatar_url);
                this.tenants = res.data.user.tenants;
            });


        })();
    }
}

export default HeadingController;
