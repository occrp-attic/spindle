
libSpindle.factory('metadataService', ['$http', '$q', 'spindleConfig', 'schemaService',
    function($http, $q, spindleConfig, schemaService) {
  var dfd = $q.defer(),
      rolesDfd = null;

  var loadSchemas = function(metadata) {
    // After getting the metadata, resolve the list of used schemas into
    // actual objects.
    var schemaDfds = [];
    for (var i in metadata.schemas) {
      var uri = metadata.schemas[i];
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
  };

  if (spindleConfig.metadata) {
    loadSchemas(spindleConfig.metadata);
  } else {
    $http.get(spindleConfig.apiUrl + '/metadata').then(function(res) {
      loadSchemas(res.data);
    }, function(err) {
      dfd.reject(err);
    });  
  }

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
