
schwifty.directive('searchFacet', ['$http', 'metadataService', 'query',
    function($http, metadataService, query) {
  return {
    restrict: 'E',
    scope: {
      'results': '=',
      'facet': '@',
      'title': '@',
      'type': '@'
    },
    templateUrl: 'search_facet.html',
    link: function (scope, element, attrs, model) {
      scope.result = [];
      scope.meta = {};
      scope.query = query;

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
