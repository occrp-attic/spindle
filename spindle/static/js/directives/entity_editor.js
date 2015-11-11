
spindle.directive('entityEditor', ['$http', '$document', 'authz', 'schemaService', 'metadataService',
    function($http, $document, authz, schemaService, metadataService) {
  return {
    restrict: 'E',
    transclude: false,
    scope: {
      'model': '=',
      'collection': '='
    },
    templateUrl: 'entities/editor.html',
    controller: ['$scope', function($scope) {

      var apiUrl = '/api/collections/' + $scope.collection.id + '/entities';
      $scope.editable = authz.collection(authz.WRITE, $scope.collection.id);

      var selectedRow = null, selectedCell = null;

      $scope.selectRow = function(rowIdx) {
        if (selectedRow == rowIdx) {
          return;
        }
        selectedRow = rowIdx;
        for (var i in $scope.rows) {
          if ($scope.rows[i].edit) {
            $scope.saveRow(i);
          }
          $scope.rows[i].edit = i == rowIdx;
        }
      };

      $scope.isCellSelected = function(rowIdx, cellIdx) {
        return rowIdx == selectedRow && cellIdx == selectedCell;
      };

      $scope.selectCell = function(rowIdx, cellIdx, $event) {
        selectedCell = cellIdx;
        $scope.selectRow(rowIdx);
        if ($event) {
          $event.stopPropagation();  
        }
      };

      $scope.saveRow = function(idx) {
        console.log('Save!');
      };

      angular.element($document).on('click', function(event) {
        // this will listen to all clicks and blur the current cell when
        // it happens outside the editor.
        if (!$(event.target).closest('.entity-editor-cell').length) {
          if (selectedCell != null || selectedRow != null) {
            $scope.selectCell(null, null)
            $scope.$apply();  
          }
        }
      });

      var loadData = function() {
        var params = {$schema: $scope.model.schema.id};
        return $http.get(apiUrl, {params: params});
      };

      var getModelColumns = function(model, metadata) {
        var columns = [], models = model.getPropertyModels().sort(spindleModelSort);
        for (var i in models) {
          var model = models[i],
              hidden = model.schema.hidden || model.isArray || model.schema.inline;
          if (!hidden) {
            columns.push({
              title: model.getTitle(),
              model: model
            });  
          }
        }
        return columns;
      };

      var getRows = function(columns, entities) {
        var rows = []
        for (var i in entities.results) {
          var entity = entities.results[i], cells = [];
          for (var j in columns) {
            var column = columns[j], value = entity[column.model.name];
            cells.push(schemaService.bindModel(value, column.model));
          }
          rows.push({
            cells: cells,
            data: entity,
            edit: false
          });
        }
        return rows;
      };

      var addStubRow = function() {
        var cells = [];
        for (var j in $scope.columns) {
          var column = $scope.columns[j];
          cells.push(schemaService.bindModel(undefined, column.model));
        }
        $scope.rows.push({
          cells: cells,
          data: {},
          edit: false
        });
      };

      var init = function() {
        metadataService.get().then(function(metadata) {
          loadData().then(function(res) {
            $scope.columns = getModelColumns($scope.model, metadata);
            $scope.rows = getRows($scope.columns, res.data);
            for (var i in [1, 2, 3, 4]) {
              addStubRow();
            }
          });
        });
      };

      init();
    }]
  };
}]);
