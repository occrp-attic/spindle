var libSpindleConfig = angular.module('libSpindleConfig', []);
var SpindleConfig = SpindleConfig || {};

libSpindleConfig.factory('spindleConfig', function() {
  console.log('SpindleConfig:', SpindleConfig);
  return {
    apiUrl: SpindleConfig.apiUrl || '/api',
    metadata: SpindleConfig.metadata,
    entities: SpindleConfig.entities || [],
    schemas: SpindleConfig.schemas || {},
    raw: SpindleConfig
  };
});

var libSpindle = angular.module('libSpindle', ['libSpindleConfig']);
