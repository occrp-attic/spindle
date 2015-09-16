
schwifty.factory('metadataService', ['$http', '$q', function($http, $q) {
  var dfd = $q.defer();

  $http.get('/api/metadata').then(function(res) {
    dfd.resolve(res.data);
  });

  return {
    get: function() {
      return dfd.promise;
    }
  }
}]);

var loadMetadata = ['metadataService', function(metadataService) {
  return metadataService.get();
}];
