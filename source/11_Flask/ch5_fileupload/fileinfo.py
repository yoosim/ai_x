# 특정 폴더()안의 파일들의 정보를 불러오기
import os  #  폴더에 접근하기 위한
import datetime # 파일의 생성 날짜 정보 출력

UPLOAD_FOLDER = './uploads/'

def stamp2datetime(stamp):
	return datetime.datetime.fromtimestamp(stamp)

def info(filename):
	ctime = os.path.getctime(UPLOAD_FOLDER + filename) # 파일의 생성 날짜 출력
	mtime = os.path.getmtime(UPLOAD_FOLDER + filename) # 파일의 수정 날짜 출력
	atime = os.path.getatime(UPLOAD_FOLDER + filename) # 파일의 접근 날짜 출력
	size = os.path.getsize(UPLOAD_FOLDER + filename) # 파일의 크기 출력
	if size >= 1024 * 1024 :  # 1024*1024 보다 크면 MB로 출력
		size = size / (1024 * 1024)
		# size = '%.2f MB' % size
		size = "{:.3f}MB".format(size)
	elif size >= 1024 : # 1024 보다 크면 KB로 출력
		size = size / 1024
		# size = '%.2f KB' % size
		size = "{:.3f}KB".format(size) 
	else : # 1024 보다 작을 경우 B로 출력
		size = "{:.3f}B".format(size)
	return stamp2datetime(ctime), stamp2datetime(mtime), stamp2datetime(atime), size

if __name__ == '__main__':
	filelist = os.listdir(UPLOAD_FOLDER) # g해당 폴더의 파일 이름 목록
	for filename in filelist:
		ctime, mtime, atime, size = info(filename)
		print(filename, ctime, mtime, atime, size)

# filelist = os.listdir(UPLOAD_FOLDER) # g해당 폴더의 파일 이름 목록
# # print(filelist)
# for filename in filelist:
# 	ctime = os.path.getctime(UPLOAD_FOLDER + filename) # 파일의 생성 날짜 출력
# 	mtime = os.path.getmtime(UPLOAD_FOLDER + filename) # 파일의 수정 날짜 출력
# 	atime = os.path.getatime(UPLOAD_FOLDER + filename) # 파일의 접근 날짜 출력
# 	size = os.path.getsize(UPLOAD_FOLDER + filename) # 파일의 크기 출력
# 	print(filename, ctime, mtime, atime, size)