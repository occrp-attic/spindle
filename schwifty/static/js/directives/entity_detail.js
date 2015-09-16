
schwifty.directive('entityDetail', ['$http', 'metadataService',
    function($http, metadataService) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'result': '='
    },
    templateUrl: 'entity_detail.html',
    link: function (scope, element, attrs, model) {
      scope.data = {};
      scope.source = {};
      scope.rows = []

      scope.$watch('result', function(res) {
        if (res === null) return;
        $http.get(res.uri).then(function(res) {
          scope.data = res.data.data;

          metadataService.get().then(function(meta) {
              scope.source = meta.sources[scope.data.source];
          });

          var rows = [];
          angular.forEach(scope.data.raw, function(value, key) {
            row = {value: value, header: key.split('.', 2)[1]};
            if (row.header == 'source_file') {
              return;
            }
            if (value && (value + '').trim().length > 0) {
              rows.push(row);
            }
          });
          scope.rows = rows;
        });
      });
    }
  };
}]);
