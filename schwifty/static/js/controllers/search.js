
var loadSearchResult = ['query', function(query) {
  return query.execute();
}];


schwifty.controller('SearchController', ['$scope', '$http', '$location', 'results', 'metadata', 'query',
  function($scope, $http, $location, results, metadata, query) {

  $scope.metadata = metadata;
  $scope.results = results;
  $scope.query = query;

}]);
