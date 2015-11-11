
var loadEntityResources = ['$http', '$q', '$route', 'schemaService',
    function($http, $q, $route, schemaService) {

  var dfd = $q.defer(),
      url = '/api/entities/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    schemaService.getBind(res.data.data).then(function(bind) {
      var collDfds = [];
      for (var i in bind.data.$collections) {
        var coll = bind.data.$collections[i];
        collDfds.push($http.get('/api/collections/' + coll));
      }
      $q.all(collDfds).then(function(responses) {
        var collections = [];
        for (var i in responses) {
          collections.push(responses[i].data.data);
        }
        dfd.resolve({
          bind: bind,
          collections: collections
        });  
      });
    }, function(err) {
      dfd.reject(err);
    });
  }, function(err) {
    dfd.reject(err);
  });
  return dfd.promise;
}];


spindle.controller('EntityController', ['$scope', '$http', 'entity', 'metadata',
  function($scope, $http, entity, metadata) {

  $scope.bind = entity.bind;
  $scope.collections = entity.collections;
  $scope.data = entity.bind.data;
  $scope.metadata = metadata;

  // set up sidebar fact sheet.
  var properties = [], ignore_name = ['id', 'name'];
  for (var i in entity.bind.binds) {
    var prop = entity.bind.binds[i];
    if (prop.model.isValue && !prop.model.schema.hidden && ignore_name.indexOf(prop.model.name) == -1) {
      properties.push(prop);
    }
  }
  $scope.properties = properties;

}]);
