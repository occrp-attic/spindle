var schwifty = angular.module('schwifty', ['ngRoute', 'ngAnimate']);

schwifty.config(['$routeProvider', function($routeProvider) {
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

  $routeProvider.when('/entity/:type/:id', {
    templateUrl: 'entity.html',
    controller: 'EntityController',
    reloadOnSearch: false,
    resolve: {
      entity: loadEntity,
      metadata: loadMetadata
    }
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });
}]);


schwifty.controller('AppController', ['$scope', '$rootScope', '$http', '$location', 'query',
  function($scope, $rootScope, $http, $location, query) {

  $scope.query = query;

  $rootScope.$on("$routeChangeStart", function (event, next, current) {
    query.get();
  });

  $scope.submitSearch = function(form) {
    query.set('q', $scope.query.state.q);
  };

}]);
