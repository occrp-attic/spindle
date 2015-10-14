
schwifty.factory('schema', ['$http', '$q', function($http, $q) {
  var schemaCache = {};

  var loadSchema = function(uri, schema) {
    if (!schemaCache[uri]) {
      var dfd = $q.defer()
          schemaCache[uri] = dfd.promise;
      if (schema && schema.id) {
        dfd.resolve(schema);
      } else {
        $http.get(uri).then(function(res) {
          dfd.resolve(res.data);
        });
      }
    }
    return schemaCache[uri]
  };

  function Visitor(schema) {
    this.schema = schema;
  }

  Visitor.prototype.getSchema = function() {
    var self = this;
    if (!self.schemaDfd) {
        self.schemaDfd = $q.defer();
        if (self.schema.$ref) {
          loadSchema(self.schema.$ref).then(function(schema) {
            delete self.schema.$ref;
            angular.extend(self.schema, schema)
            self.schemaDfd.resolve(self.schema);
          });
        } else {
          self.schemaDfd.resolve(self.schema);
        }
    }
    return self.schemaDfd.promise;
  };

  function Bind(obj, schema_uri) {
    this.obj = obj;
    schema_uri = schema_uri || obj.$schema;
    this.visitor = new Visitor({$ref: schema_uri});
  }

  return {
    loadSchema: loadSchema,
    getBind: function(obj, schema_uri) {
      return new Bind(obj, schema_uri);
    }
  }
}]);
