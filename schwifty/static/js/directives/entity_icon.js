
schwifty.directive('entityIcon', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'schema': '='
    },
    templateUrl: 'entity_icon.html',
    link: function (scope, element, attrs, model) {

      scope.isPerson = function() {
        return scope.schema == 'http://schema.occrp.org/generic/person.json#';
      };

      scope.isOrganization = function() {
        return scope.schema == 'http://schema.occrp.org/generic/organization.json#';
      };

      scope.isCompany = function() {
        return scope.schema == 'http://schema.occrp.org/generic/company.json#';
      };

      scope.isOther = function() {
        return !scope.isPerson() && !scope.isOrganization() && !scope.isCompany();
      };
    }
  };
}]);
