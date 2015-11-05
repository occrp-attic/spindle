
spindle.directive('searchFacet', ['$http', '$q', '$uibModal', 'metadataService', 'query',
    function($http, $q, $uibModal, metadataService, query) {
  return {
    restrict: 'E',
    scope: {
      'results': '=',
      'facet': '@',
      'title': '@',
      'type': '@'
    },
    templateUrl: 'search/facet.html',
    link: function (scope, element, attrs, model) {
      scope.result = [];
      scope.meta = {};
      scope.query = query;

      scope.editSource = function(sourceId, $event) {
        $event.stopPropagation();
        var d = $uibModal.open({
          templateUrl: 'sources/settings.html',
          controller: 'SourceSettingsDialog',
          backdrop: true,
          resolve: {
            source: function() {
              var dfd = $q.defer();
              $http.get('/api/sources/' + sourceId).then(function(res) {
                dfd.resolve(res.data.data);
              }, function(err) {
                dfd.reject(err);
              });
              return dfd.promise;
            }
          }
        });
      };

      scope.isSources = function() {
        return scope.facet == '$sources';
      }

      scope.$watch('results', function(res) {
        if (res === null) return;

        metadataService.get().then(function(meta) {
          scope.result = res.facets[scope.facet];
          scope.meta = meta[scope.type];
        });
      });
    }
  };
}]);
