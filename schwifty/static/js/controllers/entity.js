
var loadEntity = ['$http', '$q', '$route', function($http, $q, $route) {
  var dfd = $q.defer(),
      url = '/api/entity/' + $route.current.params.type + '/' + $route.current.params.id;
  $http.get(url).then(function(res) {
    var entity = res.data.data;
    entity.rows = [];
    angular.forEach(entity.raw, function(value, key) {
      row = {value: value, header: key.split('.', 2)[1]};
      if (row.header == 'source_file') {
        return;
      }
      if (value && (value + '').trim().length > 0) {
        entity.rows.push(row);
      }
    });
    dfd.resolve(entity);
  });
  return dfd.promise;
}];


schwifty.controller('EntityController', ['$scope', '$http', 'entity', 'metadata',
  function($scope, $http, entity, metadata) {

  $scope.source = metadata.sources[entity.source];
  $scope.data = entity;
  $scope.metadata = metadata;


}]);
