var spindle = angular.module('spindle', ['libSpindle', 'ngRoute', 'ngAnimate', 'pikaday',
  'duScroll', 'ui.bootstrap', 'angulartics', 'angulartics.piwik', 'infinite-scroll']);

spindle.config(['$routeProvider', '$analyticsProvider', '$compileProvider', 'pikadayConfigProvider',
    function($routeProvider, $analyticsProvider, $compileProvider, pikadayConfigProvider) {

  $routeProvider.when('/', {
    templateUrl: 'home.html',
    controller: 'HomeController',
    resolve: {
      metadata: loadMetadata,
      summary: loadSummary,
      collections: loadCollections
    }
  });

  $routeProvider.when('/search', {
    templateUrl: 'search/index.html',
    controller: 'SearchController',
    reloadOnSearch: true,
    resolve: {
      results: loadSearchResult,
      metadata: loadMetadata
    }
  });

  $routeProvider.when('/entities/:id', {
    templateUrl: 'entities/view.html',
    controller: 'EntityController',
    reloadOnSearch: false,
    resolve: {
      entity: loadEntityResources,
      metadata: loadMetadata
    }
  });

  $routeProvider.when('/collections/:id', {
    templateUrl: 'collections/view.html',
    controller: 'CollectionController',
    reloadOnSearch: true,
    resolve: {
      data: loadCollectionEditor
    }
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $compileProvider.debugInfoEnabled(false);

  pikadayConfigProvider.setConfig({
    // format: "LL",
    setDefaultDate: false,
    defaultDate: null
  });

}]);
