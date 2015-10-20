
spindle.directive('entityTable', [function() {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'bind': '=',
      'collection': '@',
      'title': '@'
    },
    templateUrl: 'entity_table.html',
    controller: ['$scope', function($scope) {
      var self = this;

      $scope.columns = [];

      $scope.$watch('bind', function(bind) {
        if (bind && bind.has($scope.collection)) {
          $scope.rows = bind.p[$scope.collection].binds;
          self.sample = $scope.rows[0];
        }
      });

      $scope.getColumnBinds = function(row) {
        var binds = [];
        for (var i in $scope.columns) {
          var column = $scope.columns[i],
              path = column.split('.');
          binds.push(self.getBindPath(row, path));
        }
        return binds;
      };

      self.getBindPath = function(bind, path) {
        var next = path.shift();
        if (!next || !next.length) {
          return bind;
        }
        var next_bind = bind.p[next];
        if (!path.length || !next_bind) {
          return next_bind;
        }
        return self.getBindPath(next_bind, path)
      };

      self.addColumn = function(column) {
        $scope.columns.push(column);
      };
    }]
  };
}]);
