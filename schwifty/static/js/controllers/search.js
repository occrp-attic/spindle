
var loadSearchResult = ['$http', '$q', '$route', 'queryState',
    function($http, $q, $route, queryState) {

  var dfd = $q.defer();
  var query = angular.copy(queryState.get());
  query['facet'] = ['source', 'schema'];
  $http.get('/api/search', {params: query}).then(function(res) {
    dfd.resolve(res.data);
  });
  return dfd.promise;

}];


schwifty.controller('SearchController', ['$scope', '$http', '$location', 'results', 'metadata',
  function($scope, $http, $location, results, metadata) {

  $scope.metadata = metadata;
  $scope.results = results;

  console.log("Get schwifty!");

  $scope.showEntity = function(result) {
    $location.path(result.uri.split('/api', 2)[1]);
  };

}]);
