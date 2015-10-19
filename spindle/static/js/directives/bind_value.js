
spindle.directive('bindValue', ['metadataService', function(metadataService) {
  return {
    restrict: 'E',
    scope: {
      'bind': '='
    },
    templateUrl: 'bind_value.html',
    link: function (scope, element, attrs, model) {
      var schema = scope.bind.schema;
      scope.value = scope.bind.data;
      scope.url = false;

      if (schema.format) {
        if (schema.format == 'country-code') {
          metadataService.get().then(function(metadata) {
            var country = metadata.countries[scope.bind.data];
            if (country) {
                scope.value = country.title;
            }
          });
        }
        if (schema.format == 'uri') {
          scope.url = true;
        }
        if (schema.format == 'date-time') {
          scope.value = moment(scope.bind.data).format('LLL');
        }
        if (schema.format == 'date') {
          scope.value = moment(scope.bind.data).format('LL');
        }
      }
    }
  };
}]);
