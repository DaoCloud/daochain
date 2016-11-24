var webpack = require('webpack');
var path    = require('path');
var config  = require('./webpack.config');
var extend = require('lodash/extend');

config.output = {
  filename: '[name].bundle.js',
  publicPath: '',
  path: path.resolve(__dirname, 'dist')
};

var DEFAULT_ENV = {
  API_URL: '"http://api.daocloud.co"',
  LOCAL_URL: '"/api"',
  WEB3_URL: '"/"',
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
  // Reduces bundles total size
  new webpack.optimize.UglifyJsPlugin({
    mangle: {

      // You can specify all variables that should not be mangled.
      // For example if your vendor dependency doesn't use modules
      // and relies on global variables. Most of angular modules relies on
      // angular global variable, so we should keep it unchanged
      except: ['$super', '$', 'exports', 'require', 'angular']
    }
  })
]);

module.exports = config;
