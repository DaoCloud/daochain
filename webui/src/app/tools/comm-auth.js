/**
 * Created by yeting on 16/5/7.
 */

import angular from 'angular';
import $ from 'jquery';
import 'jquery.cookie';

const ApiUrl = process.env.DAOCLOUD_API_URL;

const daoVoiceApp = { app_id: '91af7bf3' };
// let token = 'IjhjZTU5MmUyLWQzNzEtNDRhNi04NGQ4LTMxOGY0YjVhZGNhMyI.Cgx-_g.ObY35TC0yaw-yNwBV9c_yv99AKQ';
let token = $.cookie('token');

// for auth promise
let authResolve;
let authReject;
const AuthPromise = new Promise((resolve, reject) => {
    authResolve = resolve;
    authReject = reject;
});

const initIfDaoVoice = () => {
    if (!window.daovoice) {
        return
    }

    daovoice('init', daoVoiceApp);
    daovoice('update');
};
const updateIfDaoVoice = (people) => {
    if (!window.daovoice) {
        return;
    }

    let _people = Object.assign({}, daoVoiceApp, people);

    daovoice('update', _people);

};
const getTokenSuccess = (res) => {
    if (!res.user.tenant) {
        return;
    }

    let user = res.user;
    let create_at_time = user.created_at;
    let user_name = user.tenant.tenant_name;
    let user_id = user.user_id;

    const getUserSuccess = (res) => {

        let email = null;

        for (let i = 0; i < res.user.connections.length; i++) {
            if (res.user.connections[i]['connect_type'] == 'email') {
                email = res.user.connections[i]['connect_value'];
                break;
            }
        }

        let authUser = {
            username: user_name,
            userId: user_id,
            email: email
        };

        authResolve(authUser);
        updateIfDaoVoice({
            user_id: user_id, // REQUIRED: 该用户在您系统上的唯一ID
            email: email, // REQUIRED:  该用户在您系统上的主邮箱
            name: user_name, // REQUIRED: 用户名
            signed_up: create_at_time // OPTIONAL: 用户的注册时间，用Unix时间戳表示
        })
    };
    const getUserError = () => {
        initIfDaoVoice();
        authReject();
    };

    $.ajax({
        url: ApiUrl + '/users/connections',
        method: 'GET',
        headers: {
            Authorization: token
        }
    }).then(getUserSuccess, getUserError);

};
const getTokenError = (jqXHR) => {
    const status = jqXHR.status;
    if (status == 401 || status == 404) {
        $.removeCookie('token', {
            path: '/'
        });
    }
    initIfDaoVoice();
    authReject();
};

if (token) {
    $.ajax({
            url: ApiUrl + '/get-token-info',
            method: 'GET',
            headers: {
                Authorization: token
            }
        })
        .then(getTokenSuccess, getTokenError)
} else {
    authReject('no token');
}


/**
 * 检测登录状态
 * @returns {Promise}
 */
export const checkLogin = () => {
    return AuthPromise;
};