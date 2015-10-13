
var loadSearchResult = ['query', function(query) {
  return query.execute();
}];


schwifty.controller('SearchController', ['$scope', '$http', '$location', 'results', 'metadata',
  function($scope, $http, $location, results, metadata) {

  $scope.metadata = metadata;
  $scope.results = results;

}]);
