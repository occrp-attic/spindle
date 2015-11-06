

var spindleModelSort = function(a, b) {
    var aidx = a.schema.sortIndex || 0,
        bidx = b.schema.sortIndex || 0;
    // console.log(a, b, aidx, bidx);
    return bidx - aidx;
};
