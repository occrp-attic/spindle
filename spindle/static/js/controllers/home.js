
var loadSummary = ['$http', '$q', function($http, $q) {
  var dfd = $q.defer();

  var q = {
    'limit': 0,
    'facet': ['$sources', '$schema']
  };

  $http.get('/api/search', {params: q}).then(function(res) {
    dfd.resolve(res.data);
  }, function(err) {
    dfd.reject(err);
  });
  return dfd.promise;
}];


spindle.controller('HomeController', ['$scope', '$http', '$location', '$uibModal', 'summary', 'collections',
    function($scope, $http, $location, $uibModal, summary, collections) {
  $scope.collections = collections;
  $scope.summary = summary;

  $scope.newCollection = function() {
    var d = $uibModal.open({
      templateUrl: 'collections/new.html',
      controller: 'CollectionNewDialog',
      backdrop: true,
      resolve: {}
    });

    d.result.then(function(collection) {
      $location.path('/collections/' + collection.id);
    });
  };
}]);
