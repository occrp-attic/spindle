var schwifty = angular.module('schwifty', ['ngRoute', 'ui.bootstrap']);

schwifty.config(['$routeProvider',
  function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'home.html',
      controller: 'HomeController',
      reloadOnSearch: false,
      resolve: {
        results: loadSearchResult
      }
    });
}]);

var loadSearchResult = ['$http', '$q', '$route',
  function($http, $q, $route) {
  var dfd = $q.defer();
  dfd.resolve({});
  return dfd.promise;
}];

schwifty.controller('AppController', ['$scope', '$http',
  function($scope, $http) {
    
}]);

schwifty.controller('HomeController', ['$scope', '$http', 'results',
  function($scope, $http, results) {

  $scope.results = results;
  console.log("Get schwifty!");
}]);
