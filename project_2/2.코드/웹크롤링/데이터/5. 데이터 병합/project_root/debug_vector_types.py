# -*- coding: utf-8 -*-
"""
Upstage 임베딩 벡터 타입 디버깅
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_vector_types():
    """벡터 타입 확인"""
    
    api_key = os.getenv("UPSTAGE_API_KEY")
    url = "https://api.upstage.ai/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "solar-embedding-1-large-query",
        "input": ["테스트 텍스트"]
    }
    
    print("🔍 Upstage 임베딩 벡터 타입 확인...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            embedding = data["data"][0]["embedding"]
            
            print(f"✅ 임베딩 성공")
            print(f"   차원: {len(embedding)}")
            print(f"   첫 10개 값: {embedding[:10]}")
            print(f"   타입들: {[type(x).__name__ for x in embedding[:10]]}")
            
            # 타입 검사
            int_count = sum(1 for x in embedding if isinstance(x, int))
            float_count = sum(1 for x in embedding if isinstance(x, float))
            
            print(f"   정수형: {int_count}개")
            print(f"   실수형: {float_count}개")
            
            if int_count > 0:
                print("⚠️  정수형 값이 포함되어 있음 - float 변환 필요")
                
                # 변환 테스트
                converted = [float(x) for x in embedding]
                print(f"✅ 변환 후 타입들: {[type(x).__name__ for x in converted[:10]]}")
            else:
                print("✅ 모든 값이 실수형")
                
        else:
            print(f"❌ API 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 예외 발생: {e}")

if __name__ == "__main__":
    debug_vector_types()