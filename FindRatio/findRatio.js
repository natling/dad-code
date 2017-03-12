var createFindRatio = function(factors) {

  var computeRatios = function(k) {
    if(k == factors.length) {
      return [[1, 1, 1]];
    }
    var [c, m] = factors[k];
    var ratios = [];
    var subratios = computeRatios(k + 1);
    for(var sub of subratios) {
      var [r, x, y] = sub;
      y *= c**m;
      for(var i = 0; i <= m; ++i) {
        ratios.push([1.0 * x / y, x, y]);
        x *= c;
        y /= c;
      }
    }
    return ratios;
  };

  var ratios = computeRatios(0);
  ratios.sort(function(a, b) { return a[0] - b[0]; })

  return function(targetRatio) {
    // Find leftmost ratio greater than targetRatio, the result is in lo, 0<=lo<=N.
    var lo = 0, hi = ratios.length;
    while(lo < hi) {
      var mid = (lo + hi) >> 1;
      if(targetRatio < ratios[mid][0])
        hi = mid;
      else
        lo = mid + 1;
    }
    // Choose between lo and lo-1, handle corner cases lo=0 and lo=N.
    var best = lo;
    if(lo == ratios.length || (lo > 0 && targetRatio * targetRatio < ratios[lo-1][0] * ratios[lo][0])) {
      best = lo - 1;
    }
    return ratios[best];
  };
};


// Test for a few sets of factors.
var test = function(factors) {
  var n = 1;
  for(var f of factors) n *= f[0]**f[1];
  console.log(["Test findRatio for factors", factors, "n", n]);
  var findRatio = createFindRatio(factors);
  var count = 0;
  var target = 0.00001;
  while(target <= 100000) {
    count += 1;
    var [r, x, y] = findRatio(target);
    console.log([count, "target", target, "ratio", r, "ratio/target", r/target, "x", x, "y", y]);
    target *= 1.5;
  }
}

test([[2,7], [3,3], [5,2]]); // n = 86400
test([[2,2], [3,2]]); // n = 36
test([[2,1], [3,1], [5,1], [7,1], [11,1], [13,1]]); // n = 30030
