
var loadSummary = ['$http', '$q', function($http, $q) {
  var dfd = $q.defer();

  var q = {
    'limit': 0,
    'facet': ['$sources', '$schema']
  };

  $http.get('/api/search', {params: q}).then(function(res) {
    dfd.resolve(res.data);
  });
  return dfd.promise;
}];


schwifty.controller('HomeController', ['$scope', '$http', '$location', 'summary',
  function($scope, $http, $location, summary) {

  $scope.summary = summary;
}]);
