spindle.controller('SourceSettingsDialog', ['$scope', '$http', '$uibModalInstance', 'source',
    function($scope, $http, $uibModalInstance, source) {
  $scope.source = source;

  $scope.validTitle = function() {
    return $scope.source.title.length > 2;
  }

  $scope.validURL = function() {
    return $scope.source.url.length > 2;
  }

  $scope.valid = function() {
    return $scope.validTitle() && $scope.validURL();
  }

  $scope.save = function() {
    if ($scope.valid()) {
      var apiUrl = '/api/sources/' + $scope.source.id;
      $http.post(apiUrl, $scope.source).then(function(res) {
        $scope.$on('permissionsSaved', function() {
          $uibModalInstance.close(res.data.data);
        });
        $scope.$broadcast('savePermissions', res.data);
      });
    }
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('ok');
  };

}]);
