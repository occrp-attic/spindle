
var spindleModelSort = function(a, b) {
    var aidx = a.schema.sortIndex || 0,
        bidx = b.schema.sortIndex || 0;
    return bidx - aidx;
};
