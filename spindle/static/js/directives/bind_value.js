
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
          model = bind.model,
          html = '&nbsp;';
      if (bind && bind.model && bind.data) {
        var schema = bind.schema,
            value = bind.data,
            url = false,
            classes = false;
        if (model.isObject) {
          url = '#/entities/' + bind.data.id;
          value = bind.data.name;
        } else if (model.isCountry) {
          value = countries[value] ? countries[value].title : value;
        } else if (model.isURI) {
          url = value;
        } else if (model.isDateTime) {
          value = moment(value).format('LLL');
          classes = 'date-time';
        } else if (model.isDate) {
          value = moment(value).format('LL');
          classes = 'date-time';
        }

        if (url) {
          html = '<a href="' + url + '">' + value + '</a>';
        } else if (classes) {
          html = '<span class="' + classes + '">' + value + '</span>';
        } else {
          html = value + '';
        }
      }
      scope.html = $sce.trustAsHtml(html);
    }
  };
}]);
