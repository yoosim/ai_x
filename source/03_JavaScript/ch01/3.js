/*변수 선언시 ver(전역변수), let(지역변수)-한 블럭안에서만 써야 한다 , const(상수)-바뀌지 않는 수*/
sum = 0;
for(let i=1; i<=5; i++){
    sum +=i; //sum = sum+i;
    console.log('i=', i ,'일때까지 누적합은', sum);
}

console.log('for문 끝');
// console.log('i=', i ,'일때까지 누적합은', sum);