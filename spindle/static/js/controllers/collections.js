
var loadCollections = ['$q', '$http', function($q, $http) {
  var dfd = $q.defer();
  $http.get('/api/collections').then(function(res) {
    dfd.resolve(res.data);
  }, function(err) {
    dfd.reject();
  });
  return dfd.promise;
}];


spindle.controller('CollectionNewDialog', ['$scope', '$http', '$uibModalInstance',
    function($scope, $http, $uibModalInstance) {
  $scope.collection = {title: ''};

  $scope.validTitle = function() {
    return $scope.collection.title.length > 2;
  }

  $scope.create = function() {
    if ($scope.validTitle()) {
      $http.post('/api/collections', $scope.collection).then(function(res) {
        $uibModalInstance.close(res.data.data);
      });
    }
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('ok');
  };

}]);


var loadCollection = ['$q', '$http', '$route', function($q, $http, $route) {
  var dfd = $q.defer(),
      url = '/api/collections/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    dfd.resolve(res.data.data);
  }, function(err) {
    dfd.reject();
  });
  return dfd.promise;
}];


spindle.controller('CollectionController', ['$scope', '$http', 'collection',
    function($scope, $http, collection) {
  $scope.collection = collection;
  console.log("Collection", collection);
}]);
