
libSpindle.filter('date', function() {
  return function(val) {
    return moment(val).format('LL');
  };
});

libSpindle.filter('urlencode', function() {
  return window.encodeURIComponent;
});
