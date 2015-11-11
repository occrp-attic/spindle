
spindle.directive('entityEditor', ['$http', 'authz', 'schemaService', 'metadataService',
    function($http, authz, schemaService, metadataService) {
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

      var loadData = function() {
        var params = {$schema: $scope.model.schema.id};
        return $http.get(apiUrl, {params: params});
      };

      // var getModelColumns = function(model, metadata) {
      //   var columns = [],
      //       properties = model.getPropertyModels().sort(spindleModelSort);
      //   for (var i in properties) {
      //     var prop = properties[i];
      //     if (prop.schema.hidden || prop.isArray) {
      //       continue;
      //     }
      //     var column = {
      //       title: prop.getTitle(),
      //       data: prop.name,
      //       readOnly: !$scope.editable
      //     };
      //     if (prop.isValue) {
      //       if (prop.types.indexOf('integer') != -1 || prop.types.indexOf('number') != -1) {
      //         column.type = 'numeric';
      //       } else if (prop.types.indexOf('boolean') != -1 || prop.types.indexOf('bool') != -1) {
      //         column.type = 'checkbox';
      //       } else if (prop.schema.format == 'date' || prop.schema.format == 'date-time') {
      //         column.type = 'date';
      //         column.dateFormat = 'YYYY-MM-DD';
      //         column.correctFormat = true;
      //       } else if (prop.schema.format == 'country-code') {
      //         var countries = [];
      //         for (var cc in metadata.countries) {
      //           var c = metadata.countries[cc];
      //           countries.push(c);
      //         }
      //         column.type = 'handsontable',
      //         column.handsontable = {
      //           data: countries,
      //           strict: true
      //         }
      //       }
      //       // TODO countries
      //     }
      //     // TODO inline objects
      //     // TODO named objects
      //     columns.push(column);
      //   }
      //   return columns;
      // };

      var getModelColumns = function(model, metadata) {
        var columns = [], models = model.getPropertyModels().sort(spindleModelSort);
        for (var i in models) {
          var model = models[i];
          columns.push({
            title: model.getTitle(),
            model: model
          });
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
            data: entity
          });
        }
        return rows;
      };

      var init = function() {
        metadataService.get().then(function(metadata) {
          loadData().then(function(res) {
            $scope.columns = getModelColumns($scope.model, metadata);
            $scope.rows = getRows($scope.columns, res.data);  
          });
        });
      };

      init();
    }]
  };
}]);
