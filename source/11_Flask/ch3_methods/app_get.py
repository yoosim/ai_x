# pythoin -m venv .venv(가상환경 생성 방법1)
# ctrl + shift + p => select interpreter => 가상환경 만들기 => .venv로 선택 => 인터프리터경로 입력
# => 찾기(python.exe / 아나콘다 폴더에 있음) (가상환경 생성 방법2)
# python -m pip install --upgrade pip (1번 방법으로 했으면 설치해야함 / 2번 방법은 자동으로 실행 됨)
# .venv\Scripts\activate (가상환경 접근)
# pip install flask
from flask import Flask, render_template, request,abort
# flask (앱 객체 만들기) / render_template (html 랜더링) / requerst (get 방식으로 파라미너 데이터 받기)
# abort (강제로 예외발생 / 예외처리)
from models import Member
from filters import mask_password

app = Flask(__name__)

# 필터링 추가 (str -> str문자갯수만큼 *)
app.template_filter("mask_pw")(mask_password)
# @app.template_filter("mask_pw")
# def mask_password(password):
# 	return "*" * len(password)

#동적 요청 경로 (수정이나 삭제 할 때)
@app.route("/user/<name>") #, methods=['GET'] - 생략됨 ) # /user/hong
def viewfunction_handlerFunction(name):
	return f"<h1>{name}님 환영합니다</h1>"

#정적 요청 경로
@app.route("/user") # /user?name=hong
def user():
	name = request.args.get("name") # get 방식으로 파라미터 값 받기
	# name = request.args.get('name') #request.args 딕셔너리 이므로 request.args['name'] 이라고 해도 됨
	if name :
		return f"<h1>전달받은 파라미터 이름 : {name}님</h1>"
	else:
		abort(404)

@app.errorhandler(404) # 404 예외 페이지 처리
def errorhandler(error):
	return render_template("404_pageNotFound.html"), 404 

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/join_form", methods=['GET'])
def join_form():
	return render_template("1_onlyget/join.html")

@app.route("/join", methods=["GET"])
def join():
	name = request.args.get('name') #get 방식
	id = request.args.get('id')
	pw = request.args.get('pw')
	addr = request.args.get('addr')
	member = Member(name,id,pw,addr)
	return render_template("result.html", member=member)

if __name__=="__main__":
	app.run(debug=True, port=80)
