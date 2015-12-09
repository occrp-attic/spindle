
var loadCollections = ['$q', '$http', function($q, $http) {
  var dfd = $q.defer();
  $http.get('/api/collections').then(function(res) {
    dfd.resolve(res.data);
  }, function(err) {
    dfd.reject();
  });
  return dfd.promise;
}];


spindle.controller('CollectionNewDialog', ['$scope', '$http', '$uibModalInstance', 'sessionService',
    function($scope, $http, $uibModalInstance, sessionService) {
  $scope.collection = {title: ''};

  $scope.validTitle = function() {
    return $scope.collection.title.length > 2;
  }

  $scope.create = function() {
    if ($scope.validTitle()) {
      $http.post('/api/collections', $scope.collection).then(function(res) {
        // re-fetch ACLs.
        sessionService.flush().then(function() {
          $uibModalInstance.close(res.data.data);  
        });
        
      });
    }
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('ok');
  };

}]);


var loadCollectionEditor = ['$q', '$http', '$route', 'metadataService', 'schemaService',
    function($q, $http, $route, metadataService, schemaService) {

  var dfd = $q.defer(),
      collectionId = $route.current.params.id,
      collectionUrl = '/api/collections/' + collectionId,
      entitiesUrl = collectionUrl + '/entities';

  // load the collection.
  var collectionDfd = $http.get(collectionUrl);

  // load all schemas and make them available as models.
  metadataService.get().then(function(metadata) {
    var dfds = [];
    for (var schema in metadata.schemas) {
      dfds.push(schemaService.getModel(schema));
    }

    $q.all(dfds).then(function(models) {
      var data = {
        schema: $route.current.params.$schema,
        models: models.sort(spindleModelSort),
        metadata: metadata,
        model: null
      };

      for (var i in data.models) {
        var model = data.models[i];
        if (data.schema == model.schema.id) {
          data.model = model;
        }
      }

      if (data.model === null) {
        data.model = data.models[0];
        data.schema = data.model.schema.id;
      }

      var entitiesDfd = $http.get(entitiesUrl, {params: {$schema: data.schema}});

      $q.all([collectionDfd, entitiesDfd]).then(function(res) {
        data.collection = res[0].data.data;
        data.entities = res[1].data.results;
        dfd.resolve(data);
      });
    }, function(err) {
      dfd.reject(err);
    });
  });
  return dfd.promise;
}];


spindle.controller('CollectionController', ['$scope', '$http', '$location', '$uibModal', 'data', 'authz',
    function($scope, $http, $location, $uibModal, data, authz) {
  $scope.collection = data.collection;
  $scope.model = data.model;
  $scope.models = data.models;
  $scope.entities = data.entities;
  $scope.editable = authz.collection(authz.WRITE, data.collection.id);

  $scope.setModel = function(model) {
    $location.search({$schema: model.schema.id});
  };
    
  $scope.editSettings = function() {
    var d = $uibModal.open({
      templateUrl: 'collections/settings.html',
      controller: 'CollectionSettingsDialog',
      backdrop: true,
      resolve: {
        collection: function() {
          return angular.copy($scope.collection);
        }
      }
    });

    d.result.then(function(collection) {
      $scope.collection = collection;
    });
  };

}]);


spindle.controller('CollectionSettingsDialog', ['$scope', '$http', '$uibModalInstance', 'collection',
    function($scope, $http, $uibModalInstance, collection) {
  $scope.collection = collection;

  $scope.validTitle = function() {
    return $scope.collection.title.length > 2;
  }

  $scope.save = function() {
    if ($scope.validTitle()) {
      var apiUrl = '/api/collections/' + $scope.collection.id;
      $http.post(apiUrl, $scope.collection).then(function(res) {
        $scope.$on('permissionsSaved', function() {
          $uibModalInstance.close(res.data.data);
        });
        $scope.$broadcast('savePermissions', res.data);
      });
    }
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('ok');
  };

}]);
