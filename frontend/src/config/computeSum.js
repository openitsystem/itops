export default class computedSum {
    constructor(array, sum, tolerance, targetCount) {
        this.array = array;
        this.sum = sum;
        this.tolerance = tolerance;
        this.targetCount =targetCount
        this.r = [];
    }

    getCombination() {   
        (function f(t,a,n) {
            if (n==0) {
                return this.r.push(t);
            }
            for (var i=0,l=a.length; i<=l-n; i++)
            {
                f(t.concat(a[i]), a.slice(i+1), n-1);
            }
        })([], this.arr, this.num);
        return this.r;
    }

    getArrayIndex() {
        var i = 0,r = [];
        for(i = 0;i<this.array.length;i++){
            this.r.push(i);
        }
  
        return this.r;
    }

    init() {
        //clone array
        var _array = this.array.concat(),i = 0;
        //sort by asc
        _array.sort(function(a,b){
          return a - b;
        });
        //get all number when it's less than or equal sum
        for(i = 0;i<_array.length;i++){
          if(_array[i] <= this.sum){
            r.push(_array[i]);
          }else{
            break;
          }
        }
  
        return r;
      }

      core (r){
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
        combArray = this.getCombination(this.arrayIndex, this.count);
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
  
        this.core(array,sum,arrayIndex,count-1,r);
      }
}
