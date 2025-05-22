/* 파이썬 객체 만들기 
    class Person : 
    def __init__(name):
        self.name = name
p = Person('홍길동')
*/
const person = {'name':'홍길동', 'age':20};
console.log('person :',person['name'],', age :', person['age']);
console.log('person :',person.name)
const arr = ['홍길동',20]; //{0:'홍길동' , 1:20}
console.log(arr[0], arr[1]); //배열은 index가 key값
