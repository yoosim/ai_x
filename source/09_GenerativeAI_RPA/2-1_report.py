# 엑셀도 열고 시트 2개 열고 openai client객체 생성, gpt4.1-nano 100자 요약
import xlwings as xw
from dotenv import load_dotenv
from openai import OpenAI
from naver_openai_api import aiconn, get_openai_shopping_analysis
load_dotenv('.env')

# 1. excel 열기
wb = xw.Book('genai_rpa.xlsx')

# 2. prev_list, now_list 시트 전체 내용 불러오기
prev_sheet = wb.sheets['prev_list']
now_sheet = wb.sheets['now_list']
prev_data = prev_sheet.used_range.value # 사용된 범위의 데이터
now_data = now_sheet.used_range.value 
# print(prev_data)
# print(now_data)

# 3. prompt 작성하기
prompt = f"""다음 두 목록을 비교분석하여, prev_list 목록에서 now_list목록으로 바뀐 주요특징을 추출해줘.
prev_list 목록 : {prev_data}
now_list 목록 : {now_data}
비교 분석 결과를 바탕으로 구체적인 수치, 상품명, 쇼핑몰명 등을 언급하여 한글 100자 이내로 분석요약해줘."""

# 4. LLM 요청하여 메세지 받기
client = OpenAI()
completion = client.chat.completions.create(
	model='gpt-4.1-nano',
	messages=[{'role':'user','content':prompt}],
	# max_tokens=300
)

# 5. 100자 요약 출력
print('분석글 :',completion.choices[0].message.content)
print('토근수 :',completion)