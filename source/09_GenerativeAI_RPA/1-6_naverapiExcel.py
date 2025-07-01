# 네이버 쇼핑 목록 데이터프레임으로 
from naver_openai_api import get_naver_api_data, str_json_dataframe
import xlwings as xw
import handelsheet as hs

def main():
  # 1. genai_rap.xls 파일 열기
  file_path = "genai_rpa.xlsx"
  wb = xw.Book(file_path)
  
  # 2~4  백업 / 'prev_list' 삭제 / 'now_list' 복사 -> 'prev_list'이름변경 / 
  hs.handle_init_sheet(file_path=file_path, wb=wb)
  
  # 5. 네이버 api 쇼핑목록 데이터 출력(json형태str->dict->dataframe)
  str_data = get_naver_api_data("shop", "애견용품")
  df_shopping = str_json_dataframe(str_data)
  
  # 6. 'now_list'시트의 모든 내용을 클리어하고, df_shopping내용('A1'셀)을 업데이트
  hs.update_now_list(wb, df_shopping)

  # 7. 파일 저장 및 닫기
  hs.save_close_file(file_path,wb)
  
if __name__=='__main__':
  main()