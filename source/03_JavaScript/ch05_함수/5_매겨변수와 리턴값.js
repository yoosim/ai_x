console.log(pow(5,3));
//선언된 매개변수보다 많은 매개변수를 호출하기 / 2개만 선언이 되었기에 그 뒤에 값은 무시됨
console.log(pow(5,2,12));
//선언된 매개변수보다 적은 매개변수를 호출하기 / 2개가 선언이 되었는데 1개만 되어있어 무시가 됨. 
console.log(pow(5));
console.log(pow());
function pow(x,y){
  //x의 y승을 return
  console.log('함수내의 x=',x,'/y=',y);
  var result = 1;
  for(let cnt=1; cnt<=y ;cnt++){ //undefined면 계산이 안 되어서 cnt=1이 result값으로 되어서 1이 출력이 됨. 
    result *=x; // result = result*x; x를 y번 곱하라
  }
  // return result; return이 없으면 undefined를 받음
}