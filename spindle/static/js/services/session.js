
spindle.factory('sessionService', ['$http', '$q', '$rootScope', function($http, $q, $rootScope) {
  var dfd = null;

  var getSession = function() {
    if (!dfd) {
      var dt = new Date(),
          config = {cache: false, params: {'_': dt.getTime()}};
      dfd = $q.defer();
      $http.get('/api/session', config).then(function(res) {
        $rootScope.session = res.data;
        dfd.resolve(res.data);
      }, function(err) {
        dfd.reject(err);
      });
    }
    return dfd.promise;
  };

  return {
    get: getSession,
    flush: function() {
      dfd = null;
      return getSession();
    }
  }
}]);

var loadSession = ['sessionService', function(sessionService) {
  return sessionService.get();
}];
