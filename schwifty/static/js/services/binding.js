
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

  function Visitor(schema, name) {
    /* The visitor helps to determine all properties that are available as
    children of a specific schema. */
    var self = this;
    self.schema = schema;
    self.name = name;

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
                    visitor = new Visitor(parent, self.name);
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

    self.getProperties = function() {
      /* A list of all properties available for the object-types schema that
      is being visited. */
      var dfd = $q.defer();
      self.getSchemaSet().then(function(schemas) {
        var properties = {};
        for (var i in schemas) {
          var schema = schemas[i];
          if (schema.properties) {
            for (var j in schema.properties) {
              if (angular.isUndefined(properties[j])) {
                properties[j] = schema.properties[j];
              }
            }
          }
        }
        dfd.resolve(properties);
      });
      return dfd.promise;
    };

    self.getType = function() {
      // Get the data type of the current element in the visitor.
      var dfd = $q.defer();
      self.getSchema().then(function(schema) {
        var types = schema.type;
        types.isObject = false;
        types.isArray = false;
        types.isValue = false;
        if (!angular.isArray(types)) {
          types = [types];
        }
        if (types.indexOf('object') != -1) {
          types.isObject = true;
        } else if (types.indexOf('array') != -1) {
          types.isArray = true;
        } else {
          types.isValue = true;
        }
        dfd.resolve(types);
      });
      return dfd.promise;
    };

    self.getChildren = function() {
      var dfd = $q.defer();
      self.getType().then(function(type) {
        if (type.isArray) {
          self.getSchema().then(function(schema) {
            var visitor = new Visitor(schema.items, self.name);
            dfd.resolve([visitor]);
          });
        } else if (type.isObject) {
          self.getProperties().then(function(properties) {
            var children = [];
            for (var name in properties) {
              var schema = properties[name];
              children.push(new Visitor(schema, name));
            }
            dfd.resolve(children);
          });
        } else {
          dfd.resolve([]);
        }
      });
      return dfd.promise;
    };

    // end visitor
  };

  function Bind(data, schema, visitor) {
    /* A bind combines a visitor (which describes the schema) with a concrete
    instance of the data and allows for simultaneous traversal of both. */
    var self = this;
    self.data = data;
    self.visitor = visitor
    if (!self.visitor) {
      schema = schema || data.$schema;
      self.visitor = new Visitor({$ref: schema});
    }

    self.getChildren = function() {
      /* Get all descendant objects or array elements which occur in both the
      data and the schema. */
      var dfd = $q.defer();
      self.visitor.getType().then(function(type) {
        self.visitor.getChildren().then(function(children) {
          var binds = [];
          if (type.isArray) {
            for (var i in self.data) {
              var item = self.data[i];
              binds.push(new Bind(item, null, children[0]));
            }
          } else if (type.isObject) {
            for (var i in children) {
              var child = children[i],
                  val = self.data[child.name];
              if (angular.isDefined(val)) {
                binds.push(new Bind(val, null, child));
              }
            }
          }
          dfd.resolve(binds);
        });
      });
      return dfd.promise;
    };

  }

  return {
    loadSchema: loadSchema,
    getBind: function(obj, schema_uri) {
      return new Bind(obj, schema_uri);
    }
  }
}]);
