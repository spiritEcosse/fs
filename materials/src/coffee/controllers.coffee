'use strict'

### Controllers ###

app_name = "item"
app = angular.module "#{app_name}.controllers", []

app.controller 'UserAddItem', ['$http', '$scope', ($http, $scope) ->
  $scope.favorite = ->
    $http.post($scope.favorite_url, {favorite_item_add: $scope.favorite_item_add}).success (data) ->
      $scope.favorite_text = data.favorite_text
      $scope.favorite_item_add = data.favorite_item_add
    .error (data) ->
      console.log('error')

  $scope.future = ->
    $http.post($scope.future_url, {future_item_add: $scope.future_item_add}).success (data) ->
      $scope.future_text = data.future_text
      $scope.future_item_add = data.future_item_add
    .error (data) ->
      console.log('error')
]
