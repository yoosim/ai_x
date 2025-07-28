# pythoin -m venv .venv(가상환경 생성 방법1)
# ctrl + shift + p => select interpreter => 가상환경 만들기 => .venv로 선택 => 인터프리터경로 입력
# => 찾기(python.exe / 아나콘다 폴더에 있음) (가상환경 생성 방법2)
# python -m pip install --upgrade pip (1번 방법으로 했으면 설치해야함 / 2번 방법은 자동으로 실행 됨)
# .venv\Scripts\activate (가상환경 접근)
# pip install flask
from flask import Flask, render_template, request # abort
# flask (앱 객체 만들기) / render_template (html 랜더링) / requerst (get 방식으로 파라미너 데이터 받기)
# abort (강제로 예외발생 / 예외처리)
from models import Member
from filters import mask_password

app = Flask(__name__)

# 필터링 추가 (str -> str문자갯수만큼 *)
app.template_filter("mask_pw")(mask_password) # filter 추가
# @app.template_filter("mask_pw")
# def mask_password(password):
# 	return "*" * len(password)

# 예외 페이지 처리
@app.errorhandler(404) # 예외 페이지 처리
def errorhandler(error):
	return render_template("404_pageNotFound.html"), 404 

@app.route("/", methods=["GET"])
def index():
	return render_template("2_postetc/index.html")

@app.route("/join", methods=['GET','POST'])
def join():
	if request.method == "GET":
		return render_template("2_postetc/join.html")
	elif request.method == "POST":
		# name = request.form.get('name') 
		# id = request.form.get('id') # id 파라미터를 type="number"보내옴
		# print(type(id)) # 
		# pw = request.form.get('pw')
		# addr = request.form.get('addr')
		member = Member(**request.form.to_dict()) # 파라미터를 dict로 변환
		# print(type(member.id)) # int
		return render_template("2_postetc/result.html", member=member)
	
@app.route("/update/<name>/<id>/<pw>/<addr>", methods=["PATCH"])
def update(name, id, pw, addr):
	print(name)
	return f"{name}님 정보가 수정되었습니다."

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
	# delete from 테이블명 where id = id를 전송해서 삭제 
	return f"id가 {id}인 정보를 삭제했습니다."
