
var loadEntity = ['$http', '$q', '$route', function($http, $q, $route, schema) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    var entity = res.data.data;
    dfd.resolve(entity);
  });
  return dfd.promise;
}];


spindle.controller('EntityController', ['$scope', '$http', 'entity', 'metadata', 'schema',
  function($scope, $http, entity, metadata, schema) {


  $scope.data = entity;
  $scope.metadata = metadata;
  $scope.jsontext = JSON.stringify(entity, null, 2);

  // test
  schema.getBind(entity).then(function(bind) {
    $scope.bind = bind;
    console.log(bind);
  });
}]);
