
var loadEntity = ['$http', '$q', '$route', 'queryState',
    function($http, $q, $route, queryState) {
  var dfd = $q.defer();
  var entityId = queryState.get().detail;
  if (entityId) {
    $http.get('/api/enitity/' + query.get().detail, {params: query}).then(function(res) {
      dfd.resolve(res.data);
    });
  } else {

  }
  return dfd.promise;

}];


schwifty.controller('SearchController', ['$scope', '$http', 'results',
  function($scope, $http, results) {

  $scope.results = results;
  console.log("Get schwifty!");

}]);
