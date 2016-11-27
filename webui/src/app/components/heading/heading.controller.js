class HeadingController {
    constructor($timeout, $http, $state, appConfig) {
        "ngInject";
        this.$timeout = $timeout;
        this.$http = $http;
        this.$state = $state;
        this.ApiUrl = appConfig.APIUrl;
        this.LocalUrl = appConfig.LocalUrl;
        this.name = 'heading';
        this.username = localStorage.getItem('username');
        this.authOrg = false;
    }

    $onInit() {
        (() => {
            this.$http({
                method: 'GET',
                url: this.ApiUrl + '/get-token-info',
                headers: {
                    'Authorization': localStorage.getItem('token')
                }
            }).then((res, status) => {
                if (!(localStorage.getItem('username') && localStorage.getItem('user-avatar'))) {
                    this.username = res.data.user.username;
                    localStorage.setItem('username', res.data.user.username);
                    localStorage.setItem('user-avatar', res.data.user.avatar_url);
                }
                this.tenants = res.data.user.tenants;

                this.$http({
                    method: 'GET',
                    url: `${this.LocalUrl}/hub/bound_addresses?local=true`,
                    headers: {
                        'Authorization': localStorage.getItem('token')
                    }
                }).then(res => {
                    this.localTenants = res.data;
                    if (!JSON.stringify(this.localTenants).split('{}').join('')) {
                        this.$state.go('init');
                    } else {
                        this.tenants.map(tenant => {
                            if (this.localTenants[tenant.tenant_name]) {
                                this.authOrg = true;
                                this.username = tenant.tenant_name;
                                localStorage.setItem('username', tenant.tenant_name);
                            }
                        });
                        if (!this.authOrg) {
                            this.$state.go('login');
                        }
                    }
                });
            });
        })();
    }
}

export default HeadingController;