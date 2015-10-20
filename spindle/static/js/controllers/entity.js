
var loadEntityBind = ['$http', '$q', '$route', 'schema', function($http, $q, $route, schema) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    schema.getBind(res.data.data).then(function(bind) {
      dfd.resolve(bind);
    }, function(err) {
      dfd.reject(err);
    });
  }, function(err) {
    dfd.reject(err);
  });
  return dfd.promise;
}];


spindle.controller('EntityController', ['$scope', '$http', 'bind', 'metadata',
  function($scope, $http, bind, metadata) {

  $scope.bind = bind;
  $scope.data = bind.data;
  $scope.metadata = metadata;

  // set up sidebar fact sheet.
  var properties = [], ignore_name = ['id', 'name'];
  for (var i in bind.binds) {
    var prop = bind.binds[i];
    if (prop.model.isValue && ignore_name.indexOf(prop.model.name) == -1) {
      properties.push(prop);
    }
  }
  $scope.properties = properties;

}]);
