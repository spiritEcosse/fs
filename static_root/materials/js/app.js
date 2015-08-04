"use strict";

var item = angular.module('item', [
    'ng.django.forms',
    'itemControllers'
]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
