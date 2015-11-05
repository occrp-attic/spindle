
spindle.factory('authz', ['$rootScope', function($rootScope) {
  return {
    collection: function(right, collection_id) {
      if ($rootScope.session.collections && $rootScope.session.collections[right]) {
        return $rootScope.session.collections[right].indexOf(collection_id) != -1;
      }
      return false;
    },
    source: function(right, source_id) {
      if ($rootScope.session.sources && $rootScope.session.sources[right]) {
        return $rootScope.session.sources[right].indexOf(source_id) != -1;
      }
      return false;
    },
    READ: 'read',
    WRITE: 'write'
  }
}]);
