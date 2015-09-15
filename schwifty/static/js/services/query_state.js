
schwifty.factory('queryState', ['$route', '$location', function($route, $location) {
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
    return query;
  };

  var set = function(name, val) {
    query = get();
    query[name] = val;
    $location.search(query);
  }

  var clear = function() {
    $location.search({});
    get();
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
    $location.search(query);
  };

  var hasFilter = function(name, val) {
    return angular.isArray(query[name]) && query[name].indexOf(val) != -1;
  };

  get();

  return {
      state: query,
      get: get,
      set: set,
      clear: clear,
      queryString: function() {
        return queryString(query);
      },
      hasFilter: hasFilter,
      toggleFilter: toggleFilter
  };

}]);
