
schwifty.directive('entityDetail', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'result': '='
    },
    templateUrl: 'entity_detail.html',
    link: function (scope, element, attrs, model) {
      scope.data = {};

      scope.$watch('result', function(res) {
        if (res === null) return;
        console.log('Result:', res);
        url = res.type + '/' + res.id;
        $http.get('/api/entity/' + url).then(function(res) {
          scope.data = res.data.data;
        });
      });
    }
  };
}]);
