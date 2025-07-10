# 플라스크릴 활용하기 위한 패키지 설치 : pip install flask
# flask라는 micro framework를 사용하기 위해
from flask import Flask
from predict import loaded_model,predict_apt_price

application = Flask(__name__) # 웹 어플리케이션 객체 생성

# 디코더
@application.route("/")
def handller_function():
    return "<h1>Hello, Flask</h1>"

# /apt/2005/186/8
# 동적 렌더링, 동적 라우팅
@application.route("/apt/<year>/<square>/<floor>")

def aptPredictHandller(year,square,floor):
    answer = predict_apt_price(year,square,floor)
    # return "<h1> 예측금액은 {} 입니다.</h1>".format(answer)
    return {'year':year,
            'squrer':square,
            'floor':floor,
            'price':answer}
if __name__=="__main__":
    #debug=True : 코드가 변경될 때마다 서버가 자동 재시작하는 옵션
    application.run(debug=True)