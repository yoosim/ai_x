# step3 : home.html  = 파일첨부화면 + 첨부했던 파일 목록 출력(다운로드 + 삭제)

from flask import Flask, render_template
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileRequired 
from werkzeug.utils import secure_filename
from fileinfo import info 
import os

from flask import send_file # 다운로드 시 필요 
from flask import redirect, url_for # 첨부한 파일 삭제 후 '/' 요청경로로 redirect

UPLOAD_FOLDER = './uploads/'

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
		# 업로드 폴더의 파일 정보를 listup
		filelist = os.listdir(UPLOAD_FOLDER) # 해당 폴더의 파일이름 목록
		infos = [] # 파일 정보(파일명, 생성시간, 수정시간, 크기) 리스트
		for filename in filelist:
			ctime, mtime, atime, size = info(filename)
			fileinfo = {'name':filename, 
							    'ctime':ctime, 
									'mtime':mtime, 
									'size':size}
			infos.append(fileinfo)
		return render_template('home.html', 
													form=form,
													infos=infos)
@app.route('/delete/<filename>')
def delete(filename):
	os.remove(UPLOAD_FOLDER + filename) # 파일 삭제 
	# return redirect(url_for('index'))
	return redirect("/") # GET방식 요청 경로

@app.route('/download/<filename>')
def download(filename):
	return send_file(UPLOAD_FOLDER + filename, 
									 as_attachment=True) # 브라우저에서 파일이 열리지않고 다운로드 하는 기능 : as_attachment=True

if __name__ == '__main__':
	app.run(debug=True)	