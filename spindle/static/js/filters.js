
spindle.filter('date', function() {
  return function(val) {
    return moment(val).format('LL');
  };
});
