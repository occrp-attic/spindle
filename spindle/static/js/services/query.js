
spindle.factory('query', ['$route', '$location', '$q', '$http', '$analytics',
    function($route, $location, $q, $http, $analytics) {
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
    query.sort = query.sort || 'score';
    query.$sources = ensureArray(query.$sources);
    query.$schema = ensureArray(query.$schema);
    query['jurisdiction_code'] = ensureArray(query['jurisdiction_code']);
    query.facet = ensureArray(query.facet);
    return query;
  };

  var set = function(name, val) {
    query = get();
    query[name] = val;
    $location.path('/search').search(query);
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
      'sort': query.sort,
      'filter:$sources': query.$sources,
      'filter:$schema': query.$schema,
      'filter:jurisdiction_code': query.jurisdiction_code,
      'facet': ['$sources', '$schema', 'jurisdiction_code']
    };
    $analytics.eventTrack('search', {
      'category': 'search',
      'label': JSON.stringify(q)
    });

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
