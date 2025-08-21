# -*- coding: utf-8 -*-
"""
샘플 보험 데이터 생성 (corpus.jsonl)
"""

import json
import os
from pathlib import Path

def create_sample_data():
    """샘플 보험 데이터 생성"""
    
    # 출력 디렉토리 생성
    output_dir = Path("./out")
    output_dir.mkdir(exist_ok=True)
    
    # 샘플 데이터
    sample_data = [
        # 보험사 연락처
        {
            "id": "contacts-0-e8de81c9",
            "source_type": "contacts",
            "title": "메리츠화재해상보험주식회사",
            "content": "주소: 서울특별시 강남구 역삼동 825-2 | 웹사이트: www.meritzfire.com | 전화: 1566-4982"
        },
        {
            "id": "contacts-1-f9ef92d0",
            "source_type": "contacts", 
            "title": "삼성화재해상보험주식회사",
            "content": "주소: 서울특별시 중구 태평로2가 70 | 웹사이트: www.samsungfire.com | 전화: 1588-5114"
        },
        {
            "id": "contacts-2-a1bf03e1",
            "source_type": "contacts",
            "title": "현대해상화재보험주식회사", 
            "content": "주소: 서울특별시 종로구 종로 33 | 웹사이트: www.hi.co.kr | 전화: 1588-5656"
        },
        {
            "id": "contacts-3-b2cf14f2",
            "source_type": "contacts",
            "title": "DB손해보험주식회사",
            "content": "주소: 서울특별시 중구 남대문로 117 | 웹사이트: www.idbins.com | 전화: 1588-0100"
        },
        
        # 사고 가이드
        {
            "id": "guide-0-c3dg25g3",
            "source_type": "guide",
            "title": "자동차 사고 신고 절차",
            "content": "1. 안전 확보: 차량을 안전한 곳으로 이동 2. 경찰 신고: 112 신고 3. 보험사 신고: 가입 보험사 콜센터 연락 4. 현장 보존: 사고 현장 사진 촬영 5. 상대방 정보 교환: 연락처, 보험사 정보 확인"
        },
        {
            "id": "guide-1-d4eh36h4", 
            "source_type": "guide",
            "title": "과실비율 결정 기준",
            "content": "과실비율은 교통사고 발생에 대한 각 당사자의 책임 정도를 백분율로 나타낸 것입니다. 신호위반, 중앙선 침범, 안전거리 미확보, 속도위반 등이 주요 판단 기준이 됩니다."
        },
        {
            "id": "guide-2-e5fi47i5",
            "source_type": "guide", 
            "title": "보험금 청구 절차",
            "content": "보험금 청구는 사고 접수 → 손해사정 → 보상 협의 → 보험금 지급 순서로 진행됩니다. 필요 서류: 사고접수증, 차량등록증, 운전면허증, 견적서, 수리비 영수증"
        },
        
        # 보험 용어
        {
            "id": "terms-0-f6gj58j6",
            "source_type": "terms",
            "title": "대인배상보험",
            "content": "자동차 사고로 다른 사람의 생명이나 신체에 피해를 입혔을 때 보상하는 의무보험입니다. 최소 1억 5천만원 이상 가입해야 하며, 무제한 가입을 권장합니다."
        },
        {
            "id": "terms-1-g7hk69k7",
            "source_type": "terms",
            "title": "대물배상보험", 
            "content": "자동차 사고로 다른 사람의 재산(차량, 건물 등)에 피해를 입혔을 때 보상하는 보험입니다. 최소 2천만원 이상 가입이 의무이며, 1억원 이상 가입을 권장합니다."
        },
        {
            "id": "terms-2-h8il70l8",
            "source_type": "terms",
            "title": "자기차량손해",
            "content": "가입자의 차량이 충돌, 화재, 도난 등으로 손해를 입었을 때 보상하는 보험입니다. 차량가액, 면책금액을 고려하여 가입하며 선택사항입니다."
        },
        
        # 뉴스
        {
            "id": "news-0-i9jm81m9",
            "source_type": "news",
            "title": "2025년 자동차보험료 인상률 3.2% 확정",
            "content": "금융감독원은 2025년 자동차보험료 참조순보험료를 평균 3.2% 인상한다고 발표했습니다. 물가상승과 수리비 증가가 주요 원인입니다. 보험사별로 차이가 있을 수 있습니다."
        },
        {
            "id": "news-1-j0kn92n0", 
            "source_type": "news",
            "title": "전기차 보험료 할인 혜택 확대",
            "content": "환경부와 보험업계는 전기차 보험료 할인 혜택을 기존 5%에서 10%로 확대하기로 했습니다. 2025년 7월부터 적용되며, 친환경차 보급 활성화가 목적입니다."
        }
    ]
    
    # JSONL 파일 생성
    output_file = output_dir / "corpus.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in sample_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✅ 샘플 데이터 생성 완료!")
    print(f"   파일: {output_file}")
    print(f"   항목 수: {len(sample_data)}")
    print(f"   소스 타입별:")
    
    source_counts = {}
    for item in sample_data:
        source_type = item['source_type']
        source_counts[source_type] = source_counts.get(source_type, 0) + 1
    
    for source_type, count in source_counts.items():
        print(f"     {source_type}: {count}개")

if __name__ == "__main__":
    create_sample_data()