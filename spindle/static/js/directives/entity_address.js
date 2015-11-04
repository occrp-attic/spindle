
spindle.directive('entityAddress', [function() {
  return {
    restrict: 'E',
    scope: {
      'bind': '='
    },
    templateUrl: 'entities/address.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
