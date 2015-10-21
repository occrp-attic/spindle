
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
      $scope.limit = 15;
      $scope.page = 1;
      $scope.total = 0;

      $scope.nextPage = function() {
        if ($scope.pageCount() <= $scope.page) {
          return null;
        }
        return $scope.page + 1;
      };

      $scope.prevPage = function() {
        if ($scope.page <= 1) {
          return null;
        }
        return $scope.page - 1;
      };

      $scope.setPage = function(page) {
        $scope.page = page;
      };

      $scope.pages = function() {
        var range = 3,
            count = $scope.pageCount(),
            pages = [],
            cand = Math.max(1, $scope.page - range),
            limit = Math.min(count, cand + (range * 2));
        while (true) {
          if (cand > 0) {
            if (cand <= limit) {
              pages.push(cand);
            } else {
              break;
            }
          }
          cand++;
        }
        return pages;
      };

      $scope.pageCount = function() {
        return Math.ceil($scope.rows.length / $scope.limit);
      }

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

      self.updateRows = function() {
        if ($scope.bind && $scope.bind.has($scope.collection)) {
          var rows = $scope.bind.p[$scope.collection].binds,
              boundRows = [];
          for (var i in rows) {
            boundRows.push(self.getColumnBinds(rows[i]));
          }
          $scope.rows = boundRows;
        }
      };

      self.addColumn = function(column) {
        columns.push(column);

        if (columns.length == parseInt($scope.columns, 10)) {
          self.updateRows();
        }
      };
    }]
  };
}]);
