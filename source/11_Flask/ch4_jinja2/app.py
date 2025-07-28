# pythoin -m venv .venv(가상환경 생성 방법1)
# python -m pip --upgrade pip install 
# 1. .venv\Scripts\activate (command prompt = ctrl+j, ctrl+`)
# 2. pip install flask

# jinja2 설치 (flask 설치시 자동으로 설치됨)
# jinja2 template 문법
# 1. 변수 {{var명}} 또는 {{var명 | 함수명}} 사용
    # 기본 제공 필터 : lower, upper, capitalize, title, length, replace, striptags, trim, escape, trim, 
		#                 int, float, string
# 2. 제어문 
# 2-1. if 제어문 (% if 조건1 %) A태그 (% elif 조건2 %) B태그 (% else %) C태그 {% endif %}
# 2-2 for 제어문
#{% for var in vars %}
#    loop.index:1부터 순번,loop.index0:0부터 순번
#    loop.first:첫번째 요소인지 여부, loop.last:마지막 요소인지 여부
#{% endfor %}
#3. 헤더나 풋터 include  {%include 'header.html'%}
#4. 서브태그 {% block 블럭명 %} 내용 {% endblock %}
#5. 주석 {% comment %} 내용 {% endcomment %}

from flask import Flask, render_template
from flask import request # 파라미터 값 접근

app = Flask(__name__,
						template_folder="templates", # 템플릿 폴더 지정
						static_folder="static")      # 정적 파일 폴더 (css, js, img,...등) 지정
@app.errorhandler(404) # 예외 처리 페이지와 로깅
def not_found(error):
	app.logger.error('없는 페이지 입니다.')
	return render_template("404.html"), 404

names_list=[] # post 방식으로 넘어온 name을 append 
@app.route('/', methods=['GET', 'POST'])
def index(name=None):
	if request.method == 'GET':
		name = None
		name_length = 0
	else:
		name = request.form.get('name') # post 방식으로 넘어온 name을 저장
		names_list.append(name.strip()) # post 방식으로 넘어온 name을 append
		name_length = len(name) # post 방식으로 넘어온 name의 길이를 저장 
	price = 12000
	return render_template("index.html",
												 name=name, 
												 name_length=name_length, 
												 price=price,
												 names_list=names_list)

if __name__ == '__main__':
	app.run(debug=True, port=8000)
	