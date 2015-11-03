
spindle.controller('CollectionCreateDialog', ['$scope', '$http', '$uibModalInstance',
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
