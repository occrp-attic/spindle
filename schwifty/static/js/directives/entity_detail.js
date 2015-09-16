
schwifty.directive('entityDetail', ['$http', 'metadataService',
    function($http, metadataService) {
  return {
    restrict: 'E',
    scope: {
      'result': '='
    },
    templateUrl: 'entity_detail.html',
    link: function (scope, element, attrs, model) {
      scope.data = {};
      scope.source = {};
      scope.rows = []

      var generateRows = function(raw) {
        var rows = [];
        angular.forEach(raw, function(value, key) {
          row = {value: value, header: key.split('.', 2)[1]};
          if (row.header == 'source_file') {
            return;
          }
          if (value && (value + '').trim().length > 0) {
            rows.push(row);
          }
        });
        return rows;
      }

      scope.$watch('result', function(res) {
        if (res === null) return;

        $http.get(res.uri).then(function(res) {
          scope.data = res.data.data;

          metadataService.get().then(function(meta) {
              scope.source = meta.sources[scope.data.source];
          });

          scope.rows = generateRows(scope.data.raw);
        });
      });
    }
  };
}]);
