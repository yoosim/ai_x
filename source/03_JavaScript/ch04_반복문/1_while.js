/*while(조건){
        반복할 명령어들;
    }


    do{ 
        반복할 명령어들;
        }while(조건);
*/

//1초 동안 while문을 몇번 실행했는지 출력

//1970.1.1부터 현재까지 계산하는 방법
var now = new Date(); //시분초연월일 
var startTime = now.getTime();
//console.log(startTime);
//while(이 시점의 currentmillsec가 startTime+1000이하인지){}
cnt = 0 //몇번 반복하는지 확인한기 위한 변수 선언
while(new Date().getTime() < startTime +1000){
    cnt++; //cnt 1 증가
}
console.log('while문 반복 횟수 :', cnt);

startTime = new Date().getTime();
cnt = 0
do{
    ++cnt;
}while(new Date().getTime() <startTime +1000);
console.log('do~while문 반복 횟수 :', cnt);