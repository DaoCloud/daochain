const extend = angular.extend;
import { isEmpty, emptyObject } from '../helper/object.js';
/**
 * 用户认证 Class
 */
class AuthService {

  /*@ngInject*/
  constructor($http, $q, AuthStoreService, appConfig, /*appState*/) {
    this.$http = $http;
    this.$q = $q;
    this.AuthStoreService = AuthStoreService;
    // this.APIUrl = appConfig.APIUrl;
    this.APIUrl = "http://api.daocloud.co";
    // this.appState = appState;

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

    /*
    if (!daocloudToken) {
      promise = this.$http.get(this.APIUrl + '/access-token');
    } else {
      const data = {
        daocloud_token: daocloudToken,
      };
      promise = this.$http.post(this.APIUrl + '/access-token', data);
    }   */
    // promise = this.$http.post(this.APIUrl + '/access-token', daocloudToken);
    promise = this.$q.when();
    return promise
      .then(response => {

        const res = {
          "access_token": "IjI2YmNjMTQ2LWFiZGItNGI2Yi04ZTZlLTA3ZTc5OTM5YTdjZSI.CwXgFw.gcZeYujLCZk5WFDaarBGg8vlqlA",
          "expires_in": 604800,
          "uid": "26bcc146-abdb-4b6b-8e6e-07e79939a7ce"
        }
        // const res = response.data;
        // if (this.getToken() !== res.access_token) {
        //   this.AuthStoreService.clean();
        // }
        //
        this.setToken(res.access_token);
        // this.setUserId(res.admin_uuid);

        return res;
      }, e => {
        this.AuthStoreService.clean();

        return this.$q.reject(e);
      });
  }

  // /**
  //  * 当前用户
  //  * @return {[type]} [description]
  //  */
  // user() {
  //   let currentUserId = this.getUserId();

  //   return this.AdminService.find(currentUserId)
  //     .then(response => response.data);
  // }

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
