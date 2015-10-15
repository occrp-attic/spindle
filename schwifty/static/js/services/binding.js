
schwifty.factory('schema', ['$http', '$q', function($http, $q) {
  var schemaCache = {}, schemata = {};
  /* JSON schema has a somewhat weird definition of inheritance which is most
  suitable to validation but is a bit off when doing data modelling. See:
  https://github.com/json-schema/json-schema/wiki/anyOf,-allOf,-oneOf,-not */
  var HIERARCHIES = ['anyOf', 'oneOf', 'allOf'];

  var loadSchema = function(uri, schema) {
    /* Fetch or cache. If a second argument is given, it will be cached
    under the given schema URI (this can be used to seed the cache). */
    if (!schemaCache[uri]) {
      var dfd = $q.defer()
          schemaCache[uri] = dfd.promise;

      // cache the actual schema as well:
      dfd.promise.then(function(schema) {
        schemata[uri] = schema;
      });

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

  var hasSchema = function(uri) {
    /* Check if a given schema is already cached locally. */
    return angular.isDefined(schemata[uri]);
  };

  var getSchema = function(uri) {
    // WARNING: this is unsafe because it assumes the schema has already
    // been fetched.
    return schemata[uri];
  };

  var reflectSchema = function(schema, parents) {
    /* Given a particular schema, this will recursively go through all
    sub-schemas defined in properties and schema inheritance and make sure
    that all of them are loaded into the local cache. */
    var dfd = $q.defer(), deps = [];

    // avoid circular recursion.
    parents = parents || new Array();
    if (schema.id) {
      if (parents.indexOf(schema.id) != -1) {
        dfd.resolve(getSchema(schema.id));
        return dfd.promise;
      } else {
        parents.push(schema.id);
      }
    }

    // the schema is a reference, fetch it and then process that instead.
    if (schema.$ref) {
      loadSchema(schema.$ref).then(function(schema) {
        reflectSchema(schema, parents).then(function(schema) {
          dfd.resolve(schema);
        });
      });
      return dfd.promise;
    }

    // if the schema inherits from other schemas, process those.
    for (var k in HIERARCHIES) {
      prop = schema[HIERARCHIES[k]] || [];
      for (var i in prop) {
        deps.push(reflectSchema(prop[i], parents));
      }
    }

    // check if this is an array object with a defined item type.
    if (schema.items) {
      deps.push(reflectSchema(schema.items, parents));
    }

    // process the local properties.
    if (angular.isObject(schema.properties)) {
      for (var name in schema.properties) {
        var prop = schema.properties[name];
        deps.push(reflectSchema(prop, parents));
      }
    }

    // wait for all sub-schema to be processed before resolving.
    $q.all(deps).then(function() {
      dfd.resolve(schema);
    });
    return dfd.promise;
  };

  function Model(schema, name) {
    /* The model helps to determine all properties that are available as
    children of a specific schema. */
    var self = this;
    self.schema = schema;
    self.name = name;

    if (self.schema.$ref) {
      // this is not conformant to JSON schema spec but needed for some
      // weird graph reverse traversal code. JSON schema would just replace
      // the $ref object with the schema object.
      angular.extend(self.schema, getSchema(self.schema.$ref));
      delete self.schema.$ref;
    }

    // utility functions for traversal.
    self.types = angular.isArray(schema.type) ? schema.type : [schema.type];
    self.isObject = self.types.indexOf('object') != -1;
    self.isArray = self.types.indexOf('array') != -1;
    self.isValue = !self.isObject && !self.isArray;

    /* Resolve the full hierarchy of JSON schemas referred to by the current
    schema. This is essentially a class hierarchy which is necessary in order
    to determine all available properties. */
    self.parents = [self];
    for (var k in HIERARCHIES) {
      prop = schema[HIERARCHIES[k]] || [];
      for (var i in prop) {
        var model = new Model(prop[i], self.name);
        self.parents = self.parents.concat(model.parents);
      }
    }

    self._properties = null;
    self._prop_models = null;
    self._items_model = null;

    self.getProperties = function() {
      /* A list of all properties available for the object-types schema that
      is being visited. */
      if (!self.isObject) {
        throw new Error("Cannot get properties on non-object.");
      }
      if (self._properties === null) {
        self._properties = {};
        for (var i in self.parents) {
          var schema = self.parents[i].schema;
          if (schema.properties) {
            for (var name in schema.properties) {
              if (angular.isUndefined(self._properties[name])) {
                var prop = schema.properties[name];
                self._properties[name] = prop;
              }
            }
          }
        }
      }
      return self._properties;
    };

    self.getPropertyModels = function() {
      /* Get a model for each property on the local object. */
      if (self._prop_models === null) {
        self._prop_models = [];
        var properties = self.getProperties();
        for (var name in properties) {
          var prop = properties[name];
          self._prop_models.push(new Model(prop, name));
        }
      }
      return self._prop_models;
    };

    self.getItemsModel = function() {
      /* Create a model for array items. */
      if (!self.isArray) {
        throw new Error("Cannot get items on non-array.");
      }
      if (self._items_model === null) {
        self._items_model = new Model(self.schema.items, self.name);
      }
      return self._items_model;
    }

    // end model
  };

  function Bind(data, model) {
    /* A bind combines a model (which describes the schema) with a concrete
    instance of the data and allows for simultaneous traversal of both. */
    var self = this;
    self.data = data;
    self.model = model;
    self.schema = model.schema;
    self.binds = [];

    /* Get all descendant objects or array elements which occur in both the
    data and the schema. */
    if (self.model.isArray) {
      for (var i in self.data) {
        self.binds.push(new Bind(self.data[i], self.model.getItemsModel()));
      }
    } else if (self.model.isObject) {
      var models = self.model.getPropertyModels();
      for (var i in models) {
        var model = models[i],
            val = self.data[model.name];
        if (angular.isDefined(val)) {
          self.binds.push(new Bind(val, model));
        }
      }
    }

    // end bind
  }

  return {
    loadSchema: loadSchema,
    getBind: function(obj) {
      var dfd = $q.defer();
      reflectSchema({$ref: obj.$schema}).then(function(schema) {
        var model = new Model(schema);
        dfd.resolve(new Bind(obj, model));
      });
      return dfd.promise;
    }
  }
}]);
