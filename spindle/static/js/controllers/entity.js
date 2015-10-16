
var loadEntity = ['$http', '$q', '$route', 'schema', function($http, $q, $route, schema) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    schema.getBind(res.data.data).then(function(bind) {
      dfd.resolve(bind);
    });
  });
  return dfd.promise;
}];


spindle.controller('EntityController', ['$scope', '$http', 'entity', 'metadata',
  function($scope, $http, entity, metadata) {

  console.log(entity);

  $scope.bind = entity;
  $scope.data = entity.data;
  $scope.metadata = metadata;
  $scope.jsontext = JSON.stringify(entity.data, null, 2);

}]);
