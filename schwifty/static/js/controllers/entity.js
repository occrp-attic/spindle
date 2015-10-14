
var loadEntity = ['$http', '$q', '$route', function($http, $q, $route, schema) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    var entity = res.data.data;
    dfd.resolve(entity);
  });
  return dfd.promise;
}];


schwifty.controller('EntityController', ['$scope', '$http', 'entity', 'metadata', 'schema',
  function($scope, $http, entity, metadata, schema) {

  $scope.bind = schema.getBind(entity);
  $scope.data = entity;
  $scope.metadata = metadata;
  $scope.jsontext = JSON.stringify(entity, null, 2);

  // test
  $scope.bind.getChildren().then(function(schemas) {
    console.log('Loaded:', schemas);

  });
}]);
