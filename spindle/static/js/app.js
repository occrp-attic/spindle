var spindle = angular.module('spindle', ['ngRoute', 'ngAnimate',
  'angulartics', 'angulartics.piwik', 'infinite-scroll',
  'RecursionHelper']);

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

  $rootScope.$on("$routeChangeSuccess", function (event, next, current) {
    $scope.query.state = query.get();
  });

  $scope.submitSearch = function(form) {
    query.set('q', $scope.query.state.q);
  };

}]);
