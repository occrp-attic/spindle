
spindle.directive('entityEditor', ['$http', 'authz', 'hotRegisterer', 'metadataService',
    function($http, authz, hotRegisterer, metadataService) {
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
      $scope.editorId = 'table' + $scope.model.schema.id;
      $scope.tableSettings = {
        stretchH: 'all',
        fixedColumnsLeft: 0,
        minSpareRows: 20,
        // manualColumnMove: true,
        colWidths: 170,
        startRows: 20,
      };

      var loadData = function() {
        var params = {$schema: $scope.model.schema.id};
        $http.get(apiUrl, {params: params}).then(function(res) {
          $scope.entities = res.data.results;
        });
      };

      var getModelColumns = function(model, metadata) {
        var columns = [],
            properties = model.getPropertyModels().sort(spindleModelSort);
        for (var i in properties) {
          var prop = properties[i];
          if (prop.schema.hidden || prop.isArray) {
            continue;
          }
          var column = {
            title: prop.getTitle(),
            data: prop.name,
            readOnly: !$scope.editable
          };
          if (prop.isValue) {
            if (prop.types.indexOf('integer') != -1 || prop.types.indexOf('number') != -1) {
              column.type = 'numeric';
            } else if (prop.types.indexOf('boolean') != -1 || prop.types.indexOf('bool') != -1) {
              column.type = 'checkbox';
            } else if (prop.schema.format == 'date' || prop.schema.format == 'date-time') {
              column.type = 'date';
              column.dateFormat = 'YYYY-MM-DD';
              column.correctFormat = true;
            } else if (prop.schema.format == 'country-code') {
              var countries = [];
              for (var cc in metadata.countries) {
                var c = metadata.countries[cc];
                countries.push(c);
              }
              column.type = 'handsontable',
              column.handsontable = {
                data: countries,
                strict: true
              }
            }
            // TODO countries
          }
          // TODO inline objects
          // TODO named objects
          columns.push(column);
        }
        return columns;
      };

      var init = function() {
        loadData();
        metadataService.get().then(function(metadata) {
          $scope.model.columns = getModelColumns($scope.model, metadata);
        });
      }

      init();
    }]
  };
}]);
