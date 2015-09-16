
schwifty.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'schema': '='
    },
    templateUrl: 'entity_icon.html',
    link: function (scope, element, attrs, model) {
      
      scope.getIcon = function() {
        if (scope.schema == 'http://schema.occrp.org/generic/person.json#') {
          return 'fa-user';
        }
        if (scope.schema == 'http://schema.occrp.org/generic/organization.json#') {
          return 'fa-university';
        }
        if (scope.schema == 'http://schema.occrp.org/generic/company.json#') {
          return 'fa-suitcase';
        }
        return 'fa-question-circle';
      };
    }
  };
}]);
