
spindle.directive('bindEdit', ['metadataService', '$timeout', function(metadataService, $timeout) {
  var countries = [], countryLabels = {};
  metadataService.get().then(function(metadata) {
    for (var code in metadata.countries) {
      countries.push({code: code, title: metadata.countries[code].title});
      countryLabels[code] =  metadata.countries[code].title;
    }
  });

  return {
    restrict: 'E',
    replace: false,
    scope: {
      'bind': '='
    },
    templateUrl: 'bind/edit.html',
    link: function (scope, element, attrs, model) {
      var bind = scope.bind,
          model = bind.model;
      scope.textEntry = !model.isTemporal && !model.isCountry && !model.isObject;
      scope.countries = countries;

      scope.formatCountry = function($model) {
        return countryLabels[$model];
      }

      scope.$on('editBind', function(e, serial) {
        if (scope.bind.serial == serial) {
          $timeout(function() {
            angular.element(element).find('input').focus();
          });
        }
      });
    }
  };
}]);
