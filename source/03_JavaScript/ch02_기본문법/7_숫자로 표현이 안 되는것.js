i = Number('');
console.log('i =', i); //0
i = parseInt(''); //NaN
console.log('i =', NaN, '타입 =', typeof(i)); //i가 숫자인데 표현이 안 되는것 
f = 10/3;
console.log('f =', f);
a = 10/0; // 무한대(infinity) 10을 0.0000000000000000001이렇게 나눔
console.log('a =', a, 'a의 타입 =', typeof(a));

console.log('i가 NaN인지 여부 :', isNaN(i)); //true
console.log('f가 NaN인지 여부 :', isNaN(f)); //false
console.log('a가 유한수인지 여부 :', isFinite(a)); //false
console.log('f가 유한수인지 여부 :', isFinite(f)); //true

