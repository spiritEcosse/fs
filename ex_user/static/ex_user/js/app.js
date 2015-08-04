(function() {
"use strict";

var profile = angular.module('profile', []);

profile.controller('Tabs', function($scope) {
	$scope.setTab = function(tab) {
		$scope.activeTab = tab;
	};

	$scope.tabClass = function(tab) {
		if (angular.isUndefined($scope.activeTab) && $scope.tabList.length > 0) {
			$scope.activeTab = $scope.tabList[0];
		}
		return $scope.activeTab === tab ? 'active' : '';
	};
});

})();