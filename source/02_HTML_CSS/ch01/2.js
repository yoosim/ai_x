// 2.js //
let name = prompt('이름을 작성해주세요.', '홍길동'); //취소 클릭시 'null'리턴
if (name != 'null' && name != '') { //입력 후 확인버튼을 클릭시 if문에 들어옴
    document.write(name + '님 반갑습니다.<br>');
}