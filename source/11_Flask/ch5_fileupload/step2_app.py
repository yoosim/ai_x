# pip install flask_wtf : 플라스크에서 폼 관리하는 기능 
  # CSRF 방어를 위해 세션을 사용하는 기능 (보호 정책 설정)
  # 쉽고 유연한 폼 적용하여 유효성 검증, input 태그 생성
from flask import Flask, render_template
from flask_wtf import FlaskForm # 유효성 검사를 위한 from 객체 생성
from flask_wtf.file import FileField, FileRequired # 파일 업로드 기능 추가
from werkzeug.utils import secure_filename # 업로드한 파일명에 특수문자를 빼서 저장
from fileinfo import info # 파일 정보 출력
import os
UPLOAD_FOLDER = './uploads/'
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # 업로드 폴더 용량 제한 (5MB)
app.config['SECRET_KEY'] = 'secret!' # 서버 시간이 많을 경우 / 세션 암호화 설정 / CSRM 보호 정책 설정을 하려면 필요

class fileForm(FlaskForm):
	files = FileField(validators=[FileRequired()]) # 파일 업로드 기능 추가
@app.route('/', methods=['GET', 'POST'])
def index():
	form = fileForm()
	if form.validate_on_submit(): # form에 요구조건에 맞게 데이터가 들어왔는지? 유효성 검사 (POST 요청이 유효하게 되었는지 확인)
		file = form.files.data # 파일 업로드 기능 추가
		# 파일명에 서버 영향을 미칠 특수문자 빼서 저장
		safe_filename = secure_filename(file.filename)
		file.save(UPLOAD_FOLDER + safe_filename) # 업로드 폴더에 파일 저장
		ctime, mtime, atime, size = info(safe_filename) # 파일 정보 출력
		return render_template("check.html", 
												 fileinfo= {'ctime':ctime,
																		'size':size})

	else: # validate_on_submit 실패 (GET 방식이거나 POST 요청이 유효하지 않은 경우)
		return render_template('upload.html', form=form) # upload.html 수정
	
if __name__ == '__main__':
	app.run(debug=True)	