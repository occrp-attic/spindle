
spindle.directive('entityBind', ['RecursionHelper', function(RecursionHelper) {
  return {
    restrict: 'E',
    scope: {
      'bind': '=',
      'metadata': '=',
      'root': '='
    },
    templateUrl: 'entity_bind.html',
    compile: function(element) {
      return RecursionHelper.compile(element, function(scope, iElement, iAttrs, controller, transcludeFn){

        scope.isRoot = function() {
          var data = scope.bind.data;
          return data && data.id && data.id == scope.root;
        }

        scope.getChildren = function() {
          return scope.bind.binds.sort(function(a, b) {
            if (a.model.name == 'name') {
              return -1;
            }
            if (b.model.name == 'name') {
              return 1;
            }
            return 0;
          });
        }

      });
    }
  };
}]);
