
spindle.directive('bindValue', ['$sce', 'metadataService', function($sce, metadataService) {
  var countries = {};
  metadataService.get().then(function(metadata) {
    countries = metadata.countries;
  });
  return {
    restrict: 'E',
    replace: false,
    scope: {
      'bind': '=',
      'link': '='
    },
    template: '<span ng-bind-html="::html"></span>',
    link: function (scope, element, attrs, model) {
      var bind = scope.bind,
          html = '<span class="empty-value">&mdash;</span>';
      if (bind && bind.model && bind.data) {
        var schema = bind.schema, value = bind.data, url = false, classes = false;
        if (bind.model.isObject) {
          url = '#/entities/' + bind.data.id;
          value = bind.data.name;
        } else if (schema.format) {
          if (schema.format == 'country-code') {
            value = countries[value] ? countries[value].title : value;
          }
          if (schema.format == 'uri') {
            url = value;
          }
          if (schema.format == 'date-time') {
            value = moment(value).format('LLL');
            classes = 'date-time';
          }
          if (schema.format == 'date') {
            value = moment(value).format('LL');
            classes = 'date-time';
          }
        }

        if (url) {
          html = '<a href="' + url + '">' + value + '</a>';
        } else if (classes) {
          html = '<span class="' + classes + '">' + value + '</span>';
        } else {
          html = value
        }
      }
      scope.html = $sce.trustAsHtml(html);
    }
  };
}]);
