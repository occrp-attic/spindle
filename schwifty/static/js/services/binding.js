
schwifty.factory('schema', ['$http', '$q', function($http, $q) {
  var schemaCache = {};

  var loadSchema = function(uri, schema) {
    /* Fetch or cache. If a second argument is given, it will be cached
    under the given schema URI (this can be used to seed the cache). */
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
    /* The visitor helps to determine all properties that are available as
    children of a specific schema. */
    var self = this;
    self.schema = schema;

    self.getSchema = function() {
      /* Resolve the schema of the current visitor, by either downloading it
      or using a copy from a local resolver cache. */
      if (angular.isUndefined(self.schemaDfd)) {
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

    self.getSchemaSet = function() {
      /* Resolve the full hierarchy of JSON schemas referred to by the current
      schema. This is essentially a class hierarchy which is necessary in order
      to determine all available properties. */
      if (angular.isUndefined(self.schemaSetDfd)) {
        self.schemaSetDfd = $q.defer();
        self.getSchema().then(function(schema) {
          // cf. https://github.com/json-schema/json-schema/wiki/anyOf,-allOf,-oneOf,-not
          var parents = [], hierarchyProps = ['anyOf', 'oneOf', 'allOf'];
          for (var k in hierarchyProps) {
            prop = schema[hierarchyProps[k]];
            if (angular.isArray(prop)) {
              for (var i in prop) {
                var parent = prop[i],
                    visitor = new Visitor(parent);
                parents.push(visitor.getSchemaSet());
              }
            }
          }

          if (parents.length > 0) {
            $q.all(parents).then(function(set) {
              var schemata = [schema];
              for (var i in set) {
                schemata = schemata.concat(set[i]);
              }
              self.schemaSetDfd.resolve(schemata);
            });
          } else {
            self.schemaSetDfd.resolve([schema]);
          }
        });
      }
      return self.schemaSetDfd.promise;
    };

    // end visitor
  };

  function Bind(obj, schema_uri) {
    var self = this;
    self.obj = obj;
    schema_uri = schema_uri || obj.$schema;
    self.visitor = new Visitor({$ref: schema_uri});
  }

  return {
    loadSchema: loadSchema,
    getBind: function(obj, schema_uri) {
      return new Bind(obj, schema_uri);
    }
  }
}]);
