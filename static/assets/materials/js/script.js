(function() {
  'use strict';

  /* Declare app level module which depends on filters, and services */
  var app, app_name;

  app_name = 'item';

  app = angular.module(app_name, [app_name + ".controllers"]);

  app.config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      return $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
  ]);

}).call(this);

(function() {
  'use strict';

  /* Controllers */
  var app, app_name;

  app_name = "item";

  app = angular.module(app_name + ".controllers", []);

  app.controller('UserAddItem', [
    '$http', '$scope', function($http, $scope) {
      $scope.favorite = function() {
        return $http.post($scope.favorite_url, {
          favorite_item_add: $scope.favorite_item_add
        }).success(function(data) {
          $scope.favorite_text = data.favorite_text;
          return $scope.favorite_item_add = data.favorite_item_add;
        }).error(function(data) {
          return console.log('error');
        });
      };
      return $scope.future = function() {
        return $http.post($scope.future_url, {
          future_item_add: $scope.future_item_add
        }).success(function(data) {
          $scope.future_text = data.future_text;
          return $scope.future_item_add = data.future_item_add;
        }).error(function(data) {
          return console.log('error');
        });
      };
    }
  ]);

}).call(this);

(function() {
  'use strict';

  /* Directives */


}).call(this);

(function() {
  'use strict';

  /* Filters */


}).call(this);

(function() {
  'use strict';

  /* Services */


}).call(this);
