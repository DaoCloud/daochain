import angular from 'angular';
import Home from './home/home';
import Heading from './heading/heading';
import Navbar from './navbar/navbar';
import Hero from './hero/hero';
import Local from './local/local';
import Login from './login/login';
import Remote from './remote/remote';
import Person from './person/person';
import Market from './market/market';
import Imagelist from './imagelist/imagelist';
import Points from './points/points';
import User from './user/user';

let componentModule = angular.module('app.components', [
  Home,
  Heading,
  Navbar,
  Hero,
  Local,
  Login,
  Remote,
  Market,
  Person,
  Points,
  Imagelist,
  User
])
.name;

export default componentModule;
