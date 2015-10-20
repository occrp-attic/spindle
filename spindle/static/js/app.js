var spindle = angular.module('spindle', ['ngRoute', 'ngAnimate',
  'angulartics', 'angulartics.piwik', 'infinite-scroll']);

spindle.config(['$routeProvider', '$analyticsProvider',
    function($routeProvider, $analyticsProvider) {

  $routeProvider.when('/', {
    templateUrl: 'home.html',
    controller: 'HomeController',
    resolve: {
      metadata: loadMetadata,
      summary: loadSummary
    }
  });

  $routeProvider.when('/search', {
    templateUrl: 'search.html',
    controller: 'SearchController',
    reloadOnSearch: true,
    resolve: {
      results: loadSearchResult,
      metadata: loadMetadata
    }
  });

  $routeProvider.when('/entity/:id', {
    templateUrl: 'entity.html',
    controller: 'EntityController',
    reloadOnSearch: false,
    resolve: {
      bind: loadEntityBind,
      metadata: loadMetadata
    }
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });
}]);


spindle.controller('AppController', ['$scope', '$rootScope', '$http', '$location', 'query',
  function($scope, $rootScope, $http, $location, query) {

  $scope.query = query;
  $scope.routeLoaded = false;
  $scope.routeFailed = false;

  $rootScope.$on("$routeChangeStart", function (event, next, current) {
    $scope.routeLoaded = false;
    $scope.routeFailed = false;
  });

  $rootScope.$on("$routeChangeSuccess", function (event, next, current) {
    $scope.query.state = query.get();
    $scope.routeLoaded = true;
  });

  $rootScope.$on("$routeChangeError", function (event, next, current) {
    $scope.routeFailed = true;
  });

  $scope.submitSearch = function(form) {
    query.set('q', $scope.query.state.q);
  };

}]);
