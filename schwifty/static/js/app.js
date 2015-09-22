var schwifty = angular.module('schwifty', ['ngRoute']);

schwifty.config(['$routeProvider', function($routeProvider) {
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
    resolve: {
      entity: loadEntity,
      metadata: loadMetadata
    }
  });

  $routeProvider.otherwise({
    redirectTo: '/search'
  });
}]);


schwifty.controller('AppController', ['$scope', '$rootScope', '$http', '$location', 'queryState',
  function($scope, $rootScope, $http, $location, queryState) {

  $scope.query = queryState;

  $rootScope.$on("$routeChangeStart", function (event, next, current) {
    queryState.get();
  });

  $scope.submitSearch = function(form) {
    $scope.query.state.detail = null;
    $location.search($scope.query.state);
  };

}]);
