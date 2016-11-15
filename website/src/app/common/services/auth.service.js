const extend = angular.extend;
import $ from 'jquery';
import { isEmpty, emptyObject } from '../helper/object.js';
/**
 * 用户认证 Class
 */
class AuthService {

    /*@ngInject*/
    constructor($http, $q, AuthStoreService, appConfig, /*appState*/ ) {
        this.$http = $http;
        this.$q = $q;
        this.AuthStoreService = AuthStoreService;
        this.APIUrl = "http://api.daocloud.co";

        // state
        this.currentUser = {};
    }

    logout() {
        this.AuthStoreService.clean();
        // this.appState.clear();
    }

    /**
     * 获取 accessToken
     * @param  {[type]} daocloudToken [description]
     * @return {[type]}               [description]
     */
    fetchToken(daocloudToken) {
        let promise;

        promise = this.$http.post(this.APIUrl + '/access-token', daocloudToken);
        return promise
            .then(response => {
                const res = response.data;
                this.setToken(res.access_token);

                return res;
            }, e => {
                this.AuthStoreService.clean();

                if (e.data.error_id === 'login.password_not_match') {
                    let errDiv = $('<div></div>');
                    let errSpan = $('<span></span>');
                    errSpan.text('用户名/密码错误');
                    errDiv.append(errSpan);
                    errDiv.addClass('errMessage');
                    errDiv.insertAfter('.header-line');
                } else if (e.data.error_id === 'check_captcha_fail') {
                    let errDiv = $('<div></div>');
                    let errSpan = $('<span></span>');
                    errSpan.text('验证码错误');
                    errDiv.append(errSpan);
                    errDiv.addClass('errMessage');
                    errDiv.insertAfter('.header-line');
                } else {
                    let errDiv = $('<div></div>');
                    let errSpan = $('<span></span>');
                    errSpan.text('未知错误，请重新登录');
                    errDiv.append(errSpan);
                    errDiv.addClass('errMessage');
                    errDiv.insertAfter('.header-line');
                }

                return this.$q.reject(e);
            });
    }

    /**
     * 获取当前缓存的用户
     * @returns {promise}
     */
    user() {
        var deferred = this.$q.defer();

        if (!this.isGuest()) {
            deferred.resolve(this.currentUser);
        } else {
            this.fetchUser()
                .then(user => {
                    deferred.resolve(user);
                })
                .catch(error => {
                    deferred.reject(error);
                });
        }

        return deferred.promise;
    }

    /**
     * 获取当前用户
     * @returns {promise}
     */
    fetchUser() {
        var deferred = this.$q.defer();

        // 检测本地token
        if (this.checkStoreToken()) {
            this.currentUserPromise(deferred);
        } else {
            deferred.reject({ error: 'no token' });
        }

        return deferred.promise;
    }

    /**
     * 获取当前用户辅助方法
     * @param deferred
     */
    currentUserPromise(deferred) {
        const currentUserId = this.getUserId();
        const promise = this.$http.get(this.APIUrl + '/admins/' + currentUserId)
            .then(d => d.data);

        promise.then(user => {
            extend(this.currentUser, user);
            deferred.resolve(this.currentUser);
        }).catch(data => {
            emptyObject(this.currentUser);
            deferred.reject(data);
        });
    }

    checkStoreToken() {
        var token = this.getToken();
        if (!token) {
            return false;
        }

        return true;
    }

    isGuest() {
        return isEmpty(this.currentUser);
    }

    isAuthenticated() {
        return this.getToken() || !isEmpty(this.currentUser);
    }

    /////////////////////////////////////////////////////////
    /// store auth info
    /////////////////////////////////////////////////////////j

    getToken() {
        // return /*this.appState.token || */ this.AuthStoreService.getToken();
        return localStorage.getItem('token');
    }

    getUserId() {
        // return this.appState.getUserId() || this.AuthStoreService.getUserId();
    }

    setToken(token) {
        // this.appState.setToken(token);
        return localStorage.setItem('token', token);
        // return this.AuthStoreService.setToken(token);
    }

    setUserId(id) {
        // this.appState.setUserId(id);
        return this.AuthStoreService.setUserId(id);
    }

}

export default AuthService;