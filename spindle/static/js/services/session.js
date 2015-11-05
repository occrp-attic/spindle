
spindle.factory('sessionService', ['$http', '$q', '$rootScope', function($http, $q, $rootScope) {
  var dfd = null;
  return {
    get: function() {
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
    },
    flush: function() {
      dfd = null;
    }
  }
}]);

var loadSession = ['sessionService', function(sessionService) {
  return sessionService.get();
}];
