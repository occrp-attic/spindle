
spindle.directive('bindEdit', ['metadataService', function(metadataService) {
  var countries = {};
  metadataService.get().then(function(metadata) {
    countries = metadata.countries;
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
    }
  };
}]);
