
spindle.factory('metadataService', ['$http', '$q', 'schema',
    function($http, $q, schema) {
  var dfd = $q.defer();

  $http.get('/api/metadata').then(function(res) {
    // After getting the metadata, resolve the list of used schemas into
    // actual objects.
    var metadata = res.data, schemaDfds = [];
    for (var i in res.data.schemas) {
      var uri = res.data.schemas[i];
      schemaDfds.push(schema.loadSchema(uri));
    }
    $q.all(schemaDfds).then(function(res) {
      metadata.schemas = {}
      for (var i in res) {
        var obj = res[i];
        // TODO: will there always be an ID?
        metadata.schemas[obj.id] = obj;
      }
      dfd.resolve(metadata);
    });
  });

  return {
    get: function() {
      return dfd.promise;
    }
  }
}]);

var loadMetadata = ['metadataService', function(metadataService) {
  return metadataService.get();
}];
