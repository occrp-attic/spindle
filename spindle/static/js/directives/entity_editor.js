
spindle.directive('entityEditor', ['$http', 'authz', 'hotRegisterer', function($http, authz, hotRegisterer) {
  return {
    restrict: 'E',
    transclude: false,
    scope: {
      'model': '=',
      'collection': '='
    },
    templateUrl: 'entities/editor.html',
    controller: ['$scope', function($scope) {
      var apiUrl = '/api/collections/' + $scope.collection.id + '/entities';
      $scope.editable = authz.collection(authz.WRITE, $scope.collection.id);
      $scope.editorId = 'table' + $scope.model.schema.id;
      $scope.tableSettings = {
        stretchH: 'all',
        fixedColumnsLeft: 1,
        minSpareRows: 20,
        manualColumnMove: true,
        colWidths: 170,
        startRows: 20,
      };

      var loadData = function() {
        var params = {$schema: $scope.model.schema.id};
        $http.get(apiUrl, {params: params}).then(function(res) {
          $scope.entities = res.data.results;
        });
      };

      var getModelColumns = function(model) {
        var columns = [],
            properties = model.getPropertyModels().sort(spindleModelSort);
        for (var i in properties) {
          var prop = properties[i];
          if (prop.schema.hidden) {
            continue;
          }
          if (prop.isValue) {
            columns.push({
              title: prop.getTitle(),
              data: prop.name,
              readOnly: !$scope.editable
            });
          }
        }
        return columns;
      };

      var init = function() {
        loadData();
        $scope.model.columns = getModelColumns($scope.model);
      }

      init();
    }]
  };
}]);
