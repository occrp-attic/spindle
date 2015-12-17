
spindle.directive('entityEditor', ['$http', '$document', '$timeout', '$rootScope', 'authz', 'schemaService', 'metadataService',
    function($http, $document, $timeout, $rootScope, authz, schemaService, metadataService) {
  return {
    restrict: 'E',
    transclude: false,
    scope: {
      'model': '=',
      'collection': '=',
      'entities': '='
    },
    templateUrl: 'entities/editor.html',
    controller: ['$scope', function($scope) {

      var apiUrl = '/api/collections/' + $scope.collection.id + '/entities';
      $scope.editable = authz.collection(authz.WRITE, $scope.collection.id);

      var selectedCell = null,
          editorDiv = angular.element(document.getElementById('entity-editor'))

      $rootScope.$on('keydown', function(e, $event) {
        if (selectedCell == null) {
          return;
        }
        var rows = $scope.rows.length - 1, columns = $scope.columns.length - 1;
        
        // press enter to go into edit mode
        if ($event.keyCode == 13) {
          if (selectedCell.editing) {
            if (selectedCell.colIdx < columns) {
              $scope.clickCell(selectedCell.rowIdx, selectedCell.colIdx + 1);
              // $scope.editCell(selectedCell);
            } else if (selectedCell.rowIdx < rows) {
              $scope.clickCell(selectedCell.rowIdx + 1, 0);
            }
          } else {
            $scope.editCell(selectedCell);
          }
          $event.preventDefault();
          $event.stopPropagation();
          return;
        }

        // press escape to leave edit mode
        if ($event.keyCode == 27) {
          if (selectedCell.editing) {
            $scope.cancelEditCell(selectedCell);
            $event.preventDefault();
            $event.stopPropagation();
          }
          return;
        }

        // press tab to go to the next field
        if ($event.keyCode == 9) {
          if ($event.altKey || $event.shiftKey) { // alt inverts the behaviour
            if (selectedCell.colIdx > 0) {
              $scope.clickCell(selectedCell.rowIdx, selectedCell.colIdx - 1);
            } else if (selectedCell.rowIdx > 0) {
              $scope.clickCell(selectedCell.rowIdx - 1, columns);
            }
          } else {
            if (selectedCell.colIdx < columns) {
              $scope.clickCell(selectedCell.rowIdx, selectedCell.colIdx + 1);
            } else if (selectedCell.rowIdx < rows) {
              $scope.clickCell(selectedCell.rowIdx + 1, 0);
            }  
          }
          $event.preventDefault();
          $event.stopPropagation();
          return;
        }

        if ($event.keyCode == 38 && !selectedCell.editing) {
          // go up.
          if (selectedCell.rowIdx > 0) {
            $scope.clickCell(selectedCell.rowIdx - 1, selectedCell.colIdx);
            $event.preventDefault();
            $event.stopPropagation();
          }
          return;
        } else if ($event.keyCode == 40 && !selectedCell.editing) {
          // go down.
          if (selectedCell.rowIdx < rows) {
            $scope.clickCell(selectedCell.rowIdx + 1, selectedCell.colIdx);
            $event.preventDefault();
            $event.stopPropagation();
          }
          return;
        } else if ($event.keyCode == 39 && !selectedCell.editing) {
          // go right.
          if (selectedCell.colIdx < columns) {
            $scope.clickCell(selectedCell.rowIdx, selectedCell.colIdx + 1);
            $event.preventDefault();
            $event.stopPropagation();
          }
          return;
        } else if ($event.keyCode == 37 && !selectedCell.editing) {
          // go left.
          if (selectedCell.colIdx > 0) {
            $scope.clickCell(selectedCell.rowIdx, selectedCell.colIdx - 1);
            $event.preventDefault();
            $event.stopPropagation();
          }
          return;
        }

        if (!selectedCell.editing && $scope.editable && !$event.altKey
            && !$event.ctrlKey && !$event.metaKey) {
          var keyId = parseInt($event.originalEvent.keyIdentifier.substring(2), 16),
              key = String.fromCharCode(keyId);
          key = $event.shiftKey ? key.toLocaleUpperCase() : key.toLocaleLowerCase();
          key = key.charCodeAt(0) == 0 ? '' : key;
          $scope.editCell(selectedCell, key);
        }
      });

      $scope.centerCell = function(cell) {
        var cellElement = angular.element(document.getElementById('cell-' + cell.serial));
        if (cellElement[0]) {
          var leftOffset = cellElement[0].offsetLeft - (cellElement[0].clientWidth * 3);
          editorDiv.scrollLeftAnimated(Math.max(0, leftOffset));
          var rect = cellElement[0].getBoundingClientRect(),
              viewportHeight = document.documentElement.clientHeight;
          var topOffset = viewportHeight / 3;
          var topScroll = Math.max(0, rect.top - topOffset + window.pageYOffset);
          $document.scrollTopAnimated(topScroll);
        }
      };

      $scope.clickCell = function(rowIdx, colIdx, $event) {
        var cell = $scope.rows[rowIdx].cells[colIdx];
        cell.rowIdx = rowIdx;
        cell.colIdx = colIdx;
        if (cell.selected) {
          $scope.editCell(cell);
        } else {
          $scope.selectCell(cell);
        }
        if ($event) {
          $event.stopPropagation();  
        } else {
          $scope.centerCell(cell);
        }
      };

      $scope.editCell = function(cell, newVal) {
        if ($scope.editable) {
          cell.editing = true;
          $scope.$broadcast('editBind', cell.serial, newVal);
        }
      };

      $scope.cancelEditCell = function(cell) {
        if ($scope.editable) {
          cell.editing = false;
          $scope.$broadcast('cancelEditBind', cell.serial);
        }
      };

      $scope.selectRow = function(rowIdx) {
        for (var i in $scope.rows) {
          if (rowIdx != undefined && i == rowIdx) {
            $scope.rows[i].selected = true;
          } else {
            $scope.rows[i].selected = false;
          }
        }
      };

      $scope.selectCell = function(cell) {
        if (selectedCell != null) {
          var idx = selectedCell.rowIdx;
          selectedCell.selected = false;  
          selectedCell.editing = false;

          $timeout.cancel($scope.rows[idx].saveTimeout);
          $scope.rows[idx].saveTimeout = $timeout(function() {
            $scope.saveRow(idx);
          }, 500);
        }
        $scope.selectRow(cell == null ? undefined : cell.rowIdx);

        if (cell != null) {
          cell.selected = true;  
        }
        selectedCell = cell;
      };

      $scope.saveRow = function(idx, forceUpdate) {
        if (!$scope.editable) return;

        var row = $scope.rows[idx],
            hasData = !!forceUpdate;

        // upgrade the schema, if applicable:
        row.data.$schema = $scope.model.schema.id;
        for (var i in row.cells) {
          var cell = row.cells[i],
              name = cell.model.name;

          if (!cell.data || cell.data.length == 0) {
            cell.data = undefined;
          }

          if (cell.data != row.data[name]) {
            hasData = true;

            // should type casting be handled here?
            if (cell.model.isFloat) {
              cell.data = parseFloat(numeral().unformat(cell.data));
            } else if (cell.model.isInteger) {
              cell.data = parseInt(numeral().unformat(cell.data), 10);
            }
          }
          row.data[name] = cell.data;
        }

        if (hasData) {
          $http.post(apiUrl, row.data).then(function(res) {
            $scope.rows[idx].failed = false;
            $scope.rows[idx].data.id = res.data.data.id;
            if (res.status == 201) { // new record
              $scope.rows.push(makeRow());
            }
          }, function(err) {
            $scope.rows[idx].failed = true;
          });  
        }
      };

      $scope.removeEntity = function(row) {
        if (!row.data.id) {
          return;
        }
        $scope.rows.splice($scope.rows.indexOf(row), 1);
        $http.delete(apiUrl, {params: {subject: row.data.id}});
      };

      angular.element($document).on('click', function(event) {
        // this will listen to all clicks and blur the current cell when
        // it happens outside the editor.
        if (!$(event.target).closest('.entity-editor-cell').length) {
          if (selectedCell != null) {
            $scope.selectCell(null);
            $scope.$apply();  
          }
        }
      });

      $scope.$on('$destroy', function() {
        $scope.selectCell(null);
      });

      $scope.$on('fillStub', function(evt, entity) {
        var cell = selectedCell;
        $scope.rows[cell.rowIdx] = makeRow(entity);
        $scope.saveRow(cell.rowIdx, true);
        $scope.clickCell(cell.rowIdx, cell.colIdx);
        $scope.rows.push(makeRow({}));
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
        var rows = [];
        var sorted = entities.sort(function(a, b) {
          var amodel = schemaService.bindModel(a, $scope.model),
              bmodel = schemaService.bindModel(b, $scope.model);
          return amodel.compareTo(bmodel);
        });
        for (var i in sorted) {
          rows.push(makeRow(sorted[i]));
        }
        return rows;
      };

      var makeRow = function(entity) {
        var cells = [], data = {
          id: entity ? entity.id : undefined,
          $schema: $scope.model.schema.id
        };
        for (var j in $scope.columns) {
          var column = $scope.columns[j];
          var value = entity ? entity[column.model.name] : undefined;
          if (value !== undefined) {
            data[column.model.name] = value;
          }
          cells.push(schemaService.bindModel(value, column.model));
        }
        return {
          cells: cells,
          data: data,
          edit: false,
          saving: false
        };
      };

      var init = function() {
        metadataService.get().then(function(metadata) {
          $scope.columns = getModelColumns($scope.model, metadata);
          $scope.rows = getRows($scope.columns, $scope.entities);
          for (var i in [1, 2, 3]) {
            $scope.rows.push(makeRow());
          }
        });
      };

      init();
    }]
  };
}]);
