'use strict';
var itemControllers = angular.module('itemControllers', []);

itemControllers.controller('UserAddItem', ['$scope', '$http',
    function($scope, $http) {
        $scope.favorite = function() {
            $http.post(
                $scope.favorite_url,
                {favorite_item_add: $scope.favorite_item_add}
            ).
                success(function(data, status, headers, config){
                    $scope.favorite_text = data.favorite_text;
                    $scope.favorite_item_add = data.favorite_item_add;
                }).
                error(function(data, status, headers, config){
                    console.log('error');
                });
        };

        $scope.future = function() {
            $http.post(
                $scope.future_url,
                {future_item_add: $scope.future_item_add}
            ).
                success(function(data, status, headers, config){
                    $scope.future_text = data.future_text;
                    $scope.future_item_add = data.future_item_add;
                }).
                error(function(data, status, headers, config){
                    console.log('error');
                });
        }
    }]);