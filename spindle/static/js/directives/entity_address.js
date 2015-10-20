
spindle.directive('entityAddress', [function() {
  return {
    restrict: 'E',
    scope: {
      'bind': '='
    },
    templateUrl: 'entity_address.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
