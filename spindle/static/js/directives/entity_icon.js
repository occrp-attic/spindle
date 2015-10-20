
spindle.directive('entityIcon', ['schema', function(schema) {
  return {
    restrict: 'E',
    scope: {
      'schema': '='
    },
    templateUrl: 'entity_icon.html',
    link: function (scope, element, attrs, model) {
      scope.icon = 'fa-question-circle';

      scope.$watch('schema', function(uri) {
        if (uri) {
          schema.loadSchema(uri).then(function(data) {
            console.log(uri, data);
            if (data.faIcon) {
              scope.icon = data.faIcon;
            }
          })
        }
      });
    }
  };
}]);
