var libSpindleConfig = angular.module('libSpindleConfig', []);
var SpindleConfig = SpindleConfig || {};

libSpindleConfig.factory('spindleConfig', function() {
  console.log('Init config:', SpindleConfig);
  return {
    apiUrl: SpindleConfig.apiUrl || '/api',
    metadata: SpindleConfig.metadata,
    entities: SpindleConfig.entities || [],
    schemas: SpindleConfig.schemas || {},
  };
});

var libSpindle = angular.module('libSpindle', ['libSpindleConfig']);

