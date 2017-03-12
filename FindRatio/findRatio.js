var createFindRatio = function(factors) {

  var computeRatios = function(k) {
    if(k == factors.length) {
      return [[1, 1, 1]];
    }
    var myratios = [];
    var subratios = computeRatios(k + 1);
    for(var i = 0; i <= factors[k][1]; ++i) {
      for(var j = 0; j < subratios.length; ++j) {
        var x = factors[k][0]**i * subratios[j][1];
        var y = factors[k][0]**(factors[k][1] - i) * subratios[j][2];
        var r = 1.0 * x / y;
        myratios.push([r, x, y]);
      }
    }
    return myratios;
  };

  var ratios = computeRatios(0);

  var findRatio = function(targetRatio) {
    var bestI = -1;
    var bestR = 0;
    for(var i = 0; i < ratios.length; ++i) {
      var ratio = ratios[i][0];
      var r = ratio > targetRatio ? ratio/targetRatio : targetRatio/ratio;
      if(bestI == -1 || r < bestR) {
        bestI = i;
        bestR = r;
      }
    }
    return ratios[bestI];
  };
  
  return findRatio;
};

var myfactors = [[2,7], [3,3], [5,2]]; // n = 86400;
var findRatio = createFindRatio(myfactors);

var test = function() {
  for(var i = 1; i <= 50; ++i) {
    var target = 0.1 * i;
    var r = findRatio(target);
    console.log([target, r]);
  }
}

// test();