
spindle.factory('sessionService', ['$http', '$q', function($http, $q) {
  var dfd = $q.defer(),
      dt = new Date(),
      config = {cache: false, params: {'_': dt.getTime()}};

  $http.get('/api/session', config).then(function(res) {
    dfd.resolve(res.data);
  }, function(err) {
    dfd.reject(err);
  });

  return {
    get: function() {
      return dfd.promise;
    }
  }
}]);

var loadSession = ['sessionService', function(sessionService) {
  return sessionService.get();
}];
