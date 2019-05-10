function getCombBySum(array,sum,tolerance,targetCount){
  var util = {
    /*
      get combination from array
      arr: target array
      num: combination item length
      return: one array that contain combination arrays
    */
    getCombination: function(arr, num) {
      var r=[];
      (function f(t,a,n)
      {
          if (n==0)
          {
              return r.push(t);
          }
          for (var i=0,l=a.length; i<=l-n; i++)
          {
              f(t.concat(a[i]), a.slice(i+1), n-1);
          }
      })([],arr,num);
      return r;
    },
    //take array index to a array
    getArrayIndex: function(array) {
      var i = 0,
        r = [];
      for(i = 0;i<array.length;i++){
        r.push(i);
      }

      return r;
    }
  },logic = {
    //sort the array,then get what's we need
    init: function(array,sum) {
      //clone array
      var _array = array.concat(),
      r = [],
      i = 0;
      //sort by asc
      _array.sort(function(a,b){
        return a - b;
      });
      //get all number when it's less than or equal sum
      for(i = 0;i<_array.length;i++){
        if(_array[i]<=sum){
          r.push(_array[i]);
        }else{
          break;
        }
      }

      return r;
    },
    //important function
    core: function(array,sum,arrayIndex,count,r){
      var i = 0,
        k = 0,
        combArray = [],
        _sum = 0,
        _cca = [],
        _cache = [];

      if(count == _returnMark){
        return;
      }
      //get current count combination
      combArray = util.getCombination(arrayIndex,count);
      for(i = 0;i<combArray.length;i++){
        _cca = combArray[i];
        _sum = 0;
        _cache = [];
        //calculate the sum from combination
        for(k = 0;k<_cca.length;k++){
          _sum += array[_cca[k]];
          _cache.push(array[_cca[k]]);
        }
        if(Math.abs(_sum-sum) <= _tolerance){
          r.push(_cache);
        }
      }

      logic.core(array,sum,arrayIndex,count-1,r);
    }

  },
    r = [],
    _array = [],
    _targetCount = 0,
    _tolerance = 0,
    _returnMark = 0;

  //check data
  _targetCount = targetCount || _targetCount;
  _tolerance = tolerance || _tolerance;

  _array = logic.init(array,sum);
  if(_targetCount){
    _returnMark = _targetCount-1;
  }

  logic.core(_array,sum,util.getArrayIndex(_array),(_targetCount || _array.length),r);

  return r;
}