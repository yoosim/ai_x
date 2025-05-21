/* array함수 : 가변인자함수(파이썬에서 튜플매개변수)
* 매개변수가 0개 : lenght가 0인 배열 생성 return
* 매개변수가 1개 : length가 매개변수만큼의 크기인 배열 생성 return
* 매개변수가 2개 이상 : 매개변수로 배열을 생성 return */
function array(){ //arguments(매개변수 배열)
  let result = [];
  if(arguments.length==1){
    //arrgumnts[0]만큼 크기읜 배열
    for(var cnt=1; cnt<=arguments-[0] ; cnt++){
      result.push(null);
    }
  }else if(arguments.length >=2){
    //arguments 의 내용으로 배열
    for (var data of arguments){
      result.push(data)
    }
    // for(var idx=0; idx<arguments.length; idx++){
    //   result.push(arguments[idx]);
    // }
  }
  return result;
}
var arr1 = array();
var arr2 = array(3);
var arr3 = array(1,2,'상')
console.log(arr1);
console.log(arr2);
console.log(arr3);
// var arr1 = array();
// var arr2 = array(2);
// arr3 = array(2,3,);
// arr4 = array(2,3,'사)');
