var spindle = angular.module('spindle', ['ngRoute', 'ngAnimate',
  'ui.bootstrap', 'angulartics', 'angulartics.piwik', 'infinite-scroll']);

spindle.config(['$routeProvider', '$analyticsProvider', '$compileProvider',
    function($routeProvider, $analyticsProvider, $compileProvider) {

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

  $compileProvider.debugInfoEnabled(false);
}]);


spindle.controller('AppController', ['$scope', '$rootScope', '$http', '$location', 'query', 'sessionService',
  function($scope, $rootScope, $http, $location, query, sessionService) {

  $scope.query = query;
  $scope.session = {'logged_in': false, 'user': {}};
  $scope.routeLoaded = false;
  $scope.routeFailed = false;

  $rootScope.$on("$routeChangeStart", function (event, next, current) {
    $scope.routeLoaded = false;
    $scope.routeFailed = false;
    $scope.routeLoadTime = new Date();
  });

  $rootScope.$on("$routeChangeSuccess", function (event, next, current) {
    $scope.query.state = query.get();
    $scope.routeLoaded = true;
    var loadTime = new Date() - $scope.routeLoadTime;
    console.log('Loaded route, took:', loadTime, 'ms');
  });

  $rootScope.$on("$routeChangeError", function (event, next, current) {
    $scope.routeFailed = true;
  });

  sessionService.get().then(function(session) {
    $scope.session = session;
  });

  $scope.submitSearch = function(form) {
    query.set('q', $scope.query.state.q);
  };

}]);
