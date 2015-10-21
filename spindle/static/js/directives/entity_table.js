
spindle.directive('entityTable', [function() {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'bind': '=',
      'collection': '@',
      'columns': '@',
      'title': '@'
    },
    templateUrl: 'entity_table.html',
    controller: ['$scope', function($scope) {
      var self = this,
          columns = [];
      $scope.rows = [];

      self.getColumnBinds = function(row) {
        var binds = [];
        for (var i in columns) {
          var bind = row.getPath(columns[i].split('.'));
          if (!bind) {
            bind = {serial: i};
          }
          binds.push(bind);
        }
        binds.serial = row.serial;
        return binds;
      };

      self.addColumn = function(column) {
        columns.push(column);

        if (columns.length == parseInt($scope.columns, 10)) {
          if ($scope.bind && $scope.bind.has($scope.collection)) {
            var rows = $scope.bind.p[$scope.collection].binds,
                boundRows = [];
            for (var i in rows) {
              boundRows.push(self.getColumnBinds(rows[i]));
            }
            $scope.rows = boundRows;
          }
        }
      };
    }]
  };
}]);
