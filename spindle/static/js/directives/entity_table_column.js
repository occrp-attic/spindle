
spindle.directive('entityTableColumn', [function() {
  return {
    restrict: 'E',
    replace: true,
    require: '^entityTable',
    scope: {
      'path': '@',
      'title': '@',
      'width': '@'
    },
    templateUrl: 'entity_table_column.html',
    link: function (scope, element, attrs, entityTable) {
      var self = this;

      scope.getTitle = function() {
        return scope.title;
      };

      scope.$watch('path', function(path) {
        entityTable.addColumn(path);
      })

    }
  };
}]);
