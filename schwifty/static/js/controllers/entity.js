
var loadEntity = ['$http', '$q', '$route', function($http, $q, $route) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    var entity = res.data.data;
    dfd.resolve(entity);
  });
  return dfd.promise;
}];


schwifty.controller('EntityController', ['$scope', '$http', 'entity', 'metadata',
  function($scope, $http, entity, metadata) {

  // $scope.source = metadata.sources[entity.source];
  $scope.data = entity;
  $scope.metadata = metadata;

  $scope.jsontext = JSON.stringify(entity, null, 2);

}]);
