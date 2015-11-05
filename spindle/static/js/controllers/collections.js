
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


spindle.controller('CollectionController', ['$scope', '$http', '$uibModal', 'collection',
    function($scope, $http, $uibModal, collection) {
  $scope.collection = collection;
  console.log("Collection", collection);

  $scope.editSettings = function() {
    var d = $uibModal.open({
      templateUrl: 'collections/settings.html',
      controller: 'CollectionSettingsDialog',
      backdrop: true,
      resolve: {
        collection: function() {
          return angular.copy($scope.collection);
        }
      }
    });

    d.result.then(function(collection) {
      $scope.collection = collection;
    });
  };
}]);


spindle.controller('CollectionSettingsDialog', ['$scope', '$http', '$uibModalInstance', 'collection',
    function($scope, $http, $uibModalInstance, collection) {
  $scope.collection = collection;

  $scope.validTitle = function() {
    return $scope.collection.title.length > 2;
  }

  $scope.save = function() {
    if ($scope.validTitle()) {
      var apiUrl = '/api/collections/' + $scope.collection.id;
      $http.post(apiUrl, $scope.collection).then(function(res) {
        $uibModalInstance.close(res.data.data);
      });
    }
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('ok');
  };

}]);
