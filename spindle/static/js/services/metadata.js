
spindle.factory('metadataService', ['$http', '$q', 'schemaService',
    function($http, $q, schemaService) {
  var dfd = $q.defer(),
      rolesDfd = null;

  $http.get('/api/metadata').then(function(res) {
    // After getting the metadata, resolve the list of used schemas into
    // actual objects.
    var metadata = res.data, schemaDfds = [];
    for (var i in res.data.schemas) {
      var uri = res.data.schemas[i];
      schemaDfds.push(schemaService.loadSchema(uri));
    }
    $q.all(schemaDfds).then(function(res) {
      metadata.schemas = {}
      for (var i in res) {
        var obj = res[i];
        // TODO: will there always be an ID?
        metadata.schemas[obj.id] = obj;
      }
      dfd.resolve(metadata);
    }, function(err) {
      dfd.reject(err);
    });
  }, function(err) {
    dfd.reject(err);
  });

  return {
    get: function() {
      return dfd.promise;
    },
    getRoles: function() {
      if (rolesDfd == null) {
        rolesDfd = $q.defer();
        $http.get('/api/roles').then(function(res) {
          rolesDfd.resolve(res.data);
        });
      }
      return rolesDfd.promise;
    }
  }
}]);

var loadMetadata = ['metadataService', function(metadataService) {
  return metadataService.get();
}];
