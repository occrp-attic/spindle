
var loadEntityBind = ['$http', '$q', '$route', 'schema', function($http, $q, $route, schema) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    schema.getBind(res.data.data).then(function(bind) {
      dfd.resolve(bind);
    });
  });
  return dfd.promise;
}];


spindle.controller('EntityController', ['$scope', '$http', 'bind', 'metadata',
  function($scope, $http, bind, metadata) {

  console.log(bind);

  $scope.bind = bind;
  $scope.data = bind.data;
  $scope.metadata = metadata;

}]);
