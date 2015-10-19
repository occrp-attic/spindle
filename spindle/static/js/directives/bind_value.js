
spindle.directive('bindValue', ['metadataService', function(metadataService) {
  return {
    restrict: 'E',
    scope: {
      'bind': '=',
      'link': '='
    },
    templateUrl: 'bind_value.html',
    link: function (scope, element, attrs, model) {
      scope.value = null;
      scope.url = false;

      scope.$watch('bind', function(bind) {
        if (!bind) {
          return;
        }

        var schema = bind.schema;
        scope.value = bind.data;

        if (schema.format) {
          if (schema.format == 'country-code') {
            metadataService.get().then(function(metadata) {
              var country = metadata.countries[bind.data];
              if (country) {
                  scope.value = country.title;
              }
            });
          }
          if (schema.format == 'uri') {
            scope.url = true;
          }
          if (schema.format == 'date-time') {
            scope.value = moment(bind.data).format('LLL');
          }
          if (schema.format == 'date') {
            scope.value = moment(bind.data).format('LL');
          }
        }
      })

    }
  };
}]);
