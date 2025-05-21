// 가변인자함수 : 매개변수의 갯수에 따라 변하는 함수. 화살표함수에서는 불가
// 바로 쓸 수 있는 내장함수 : Array()
var arr1 = [1, 2, '상',]; //자바스크립트에서 '상'뒤에 ,(컴마)뒤에 아무값이 없으면 ,(컴마)가 무시됨. 
var arr2 = Array(1,2,'상');
arr3 = [, ,] //방의 갯수가 2인 빈 배열
arr4 = Array(2);
arr5 = []; //방의 갯수가 0인 빈 배열
arr6 = Array();
console.log(arr1);
console.log(arr2);
console.log(arr3);
console.log(arr4);
console.log(arr5);
console.log(arr6);