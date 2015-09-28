
schwifty.factory('query', ['$route', '$location', '$q', '$http',
    function($route, $location, $q, $http) {
  var query = {};

  var ensureArray = function(data) {
    if (!angular.isDefined(data)) {
      return [];
    }
    return data;
  };

  var get = function() {
    query = {};
    angular.forEach($location.search(), function(v, k) {
      if (!angular.isArray(v)) {
        v = [v];
      }
      query[k] = v;
    });
    query.source = ensureArray(query.source);
    query.schema = ensureArray(query.schema);
    query['entity.jurisdiction_code'] = ensureArray(query['entity.jurisdiction_code']);
    query.facet = ensureArray(query.facet);
    return query;
  };

  var set = function(name, val) {
    query = get();
    query[name] = val;
    $location.path('/search').search(query);
    execute();
  }

  var clear = function() {
    $location.search({});
  };

  var toggleFilter = function(name, val) {
    if (!angular.isArray(query[name])) {
      query[name] = [];
    }
    var idx = query[name].indexOf(val);
    if (idx == -1) {
      query[name].push(val);
    } else {
      query[name].splice(idx, 1);
    }
    $location.path('/search').search(query);
  };

  var hasFilter = function(name, val) {
    return angular.isArray(query[name]) && query[name].indexOf(val) != -1;
  };

  var execute = function() {
    var dfd = $q.defer();

    var q = {
      'q': query.q,
      'filter:source': query.source,
      'filter:schema': query.schema,
      'filter:entity.jurisdiction_code': query['entity.jurisdiction_code'],
      'facet': ['source', 'schema', 'entity.jurisdiction_code']
    };

    $http.get('/api/search', {params: q}).then(function(res) {
      dfd.resolve(res.data);
    });
    return dfd.promise;
  };

  get();

  return {
      state: query,
      get: get,
      set: set,
      clear: clear,
      execute: execute,
      hasFilter: hasFilter,
      toggleFilter: toggleFilter
  };

}]);
