//class 만드는 방법 (파이썬과 다르게 :이 아니라 {}으로 표현)
class Student{
    constructor(name,kor,mat,eng,sci){
        this.name = name;
        this.kor = kor;
        this.mat = mat;
        this.eng = eng;
        this.sci = sci;
    }
    getSum(){
        return this.kor + this.mat + this.eng + this.sci;
    }
    getAvg(){
        return this.getSum()/4;
    }
    toString(){
        return 'name :' + this.name +
                ' kor :' + this.kor +
                ' mat :' + this.mat +
                ' eng :' + this.eng +
                ' sci :' + this.sci +
                ' sum :' + this.getSum() +
                ' avg :' + this.getAvg();
    }
} //class 
var hong = new Student('홍', 100,90,100,90);
console.log(hong.toString());
console.log(`${hong}`); //필드 달러를 통해 호출
console.log(hong); //자동 탬플릿 리터럴이 호출