spindle.directive('collectionAdd', ['$uibModal', '$http', function($uibModal, $http) {
  return {
    restrict: 'E',
    scope: {
      'subject': '=',
      'class': '@'
    },
    templateUrl: 'collection_add.html',
    link: function (scope, element, attrs) {
      scope.loaded = false;
      scope.collections = [];

      scope.toggleDropdown = function(open) {
        if (open) {
          $http.get('/api/collections').then(function(res) {
            scope.loaded = true;
            scope.collections = res.data;
          });
        }
      };

      scope.isPart = function(collection) {
        return collection.subjects.indexOf(scope.subject) != -1;
      };

      scope.toggleCollection = function(collection) {
        var idx = collection.subjects.indexOf(scope.subject);
        if (idx == -1) {
          collection.subjects.push(scope.subject);
        } else {
          collection.subjects.splice(idx, 1);
        }
        var p = $http.post('/api/collections/' + collection.id, collection);
        p.error(function(err) {
          console.log(err);
        });
        return false;
      };

      scope.newCollection = function() {
        var d = $uibModal.open({
          templateUrl: 'collection_create.html',
          controller: 'CollectionCreateDialog',
          backdrop: true,
          resolve: {}
        });

        d.result.then(function(collection) {
          scope.collections.results.push(collection);
          scope.toggleCollection(collection);
        });
      };
    }
  };
}]);
