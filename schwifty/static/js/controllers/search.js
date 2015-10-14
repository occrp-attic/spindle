
var loadSearchResult = ['query', function(query) {
  return query.execute();
}];


schwifty.controller('SearchController', ['$scope', '$http', '$location', 'results', 'metadata',
  function($scope, $http, $location, results, metadata) {

  $scope.loading = false;
  $scope.metadata = metadata;
  $scope.results = results;
  $scope.shown = results.limit + results.offset;

  $scope.loadNext = function() {
    if ($scope.loading || !$scope.results.next) {
      return;
    }
    $scope.loading = true;
    $http.get($scope.results.next).then(function(res) {
      $scope.results.next = res.data.next;
      $scope.shown = res.data.limit + res.data.offset;
      $scope.loading = false;
      $scope.results.results = $scope.results.results.concat(res.data.results);
    });
  };

}]);
