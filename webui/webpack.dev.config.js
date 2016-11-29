var webpack = require('webpack');
var path = require('path');
var config = require('./webpack.config');
var extend = require('lodash/extend');

config.output = {
    filename: '[name].bundle.js',
    publicPath: '/',
    path: path.resolve(__dirname, 'src')
};

var DEFAULT_ENV = {
    API_URL: '"https://api.daocloud.io"',
    LOCAL_URL: '"http://localhost:8000/api"',
    WEB3_URL: '"http://localhost:8545"',
};

var CURRENT_ENV = extend({}, DEFAULT_ENV);

Object.keys(CURRENT_ENV)
    .forEach(function(k) {
        if (process.env[k]) {
            CURRENT_ENV[k] = JSON.stringify(process.env[k]);
        }
    });

config.plugins = config.plugins.concat([
    new webpack.DefinePlugin({
        'process.env': CURRENT_ENV,
    }),
    // Adds webpack HMR support. It act's like livereload,
    // reloading page after webpack rebuilt modules.
    // It also updates stylesheets and inline assets without page reloading.
    new webpack.HotModuleReplacementPlugin()
]);

module.exports = config;