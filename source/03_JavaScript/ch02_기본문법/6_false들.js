// false로 간주되는 값들 : undefined, 0 , NaN, ''(빈스트링), null
// Boolean (값) ; boolean으로 형변환
// Number (값) ; number로 형변환
// String (값) ; string으로 형변환
var i;
console.log(Boolean(i)); //undefined가 false인지 확인하기 위한것 
console.log(Boolean(0));
console.log(Boolean(NaN));
console.log(Boolean(''));
console.log(Boolean(' ')); //true임 - 빈스트링이 아닌 스페이스가 있음
console.log(Boolean(null));
console.log(Boolean(Number('a')));s