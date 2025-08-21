# -*- coding: utf-8 -*-
"""
RAG 검색 엔진
사용자 질문 → Upstage 임베딩 → Pinecone 검색 → 컨텍스트 반환
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

import requests
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

@dataclass
class SearchResult:
    """검색 결과 데이터 클래스"""
    id: str
    score: float
    source_type: str
    title: str
    content: str
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'score': self.score,
            'source_type': self.source_type,
            'title': self.title,
            'content': self.content
        }

class RAGSearchEngine:
    """RAG 검색 엔진 클래스"""
    
    def __init__(self):
        # 환경변수 로드
        self.upstage_api_key = os.getenv("UPSTAGE_API_KEY")
        self.upstage_embed_url = os.getenv("UPSTAGE_EMBED_URL", "https://api.upstage.ai/v1/embeddings")
        self.upstage_model = os.getenv("UPSTAGE_MODEL", "solar-embedding-1-large-query")  # 쿼리용 ✅
        
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_index = os.getenv("PINECONE_INDEX", "insurance-documents")
        self.namespace = os.getenv("NAMESPACE", "insurance-hub")
        
        # 검증
        assert self.upstage_api_key, "UPSTAGE_API_KEY가 필요합니다"
        assert self.pinecone_api_key, "PINECONE_API_KEY가 필요합니다"
        
        # Pinecone 초기화
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = self.pc.Index(self.pinecone_index)
        
        print(f"✅ RAG 검색 엔진 초기화 완료 - Index: {self.pinecone_index}")
    
    def embed_query(self, query: str) -> List[float]:
        """
        사용자 질문을 임베딩 벡터로 변환
        
        Args:
            query: 사용자 질문
            
        Returns:
            임베딩 벡터
        """
        headers = {
            "Authorization": f"Bearer {self.upstage_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.upstage_model,
            "input": [query]  # 리스트로 전달
        }
        
        # 재시도 로직
        for attempt in range(3):
            try:
                response = requests.post(
                    self.upstage_embed_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # 🔧 벡터를 float로 변환
                    embedding = [float(x) for x in data["data"][0]["embedding"]]
                    return embedding
                else:
                    print(f"⚠️ Upstage API 오류 (시도 {attempt+1}/3): {response.status_code}")
                    print(f"응답: {response.text[:200]}")
                    
            except Exception as e:
                print(f"⚠️ 임베딩 요청 실패 (시도 {attempt+1}/3): {e}")
            
            time.sleep(1 * (attempt + 1))  # 지수 백오프
        
        raise Exception("임베딩 생성에 실패했습니다")
    
    def search_similar(
        self, 
        query_vector: List[float], 
        top_k: int = 5,
        score_threshold: float = 0.7,
        source_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """
        벡터 유사도 검색
        
        Args:
            query_vector: 질문 임베딩 벡터
            top_k: 반환할 결과 수
            score_threshold: 최소 유사도 점수
            source_filter: 소스 타입 필터 (예: "contacts", "news")
            
        Returns:
            검색 결과 리스트
        """
        # 필터 구성
        filter_dict = {}
        if source_filter:
            filter_dict["source_type"] = {"$eq": source_filter}
        
        try:
            # Pinecone 검색
            search_response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                namespace=self.namespace,
                filter=filter_dict if filter_dict else None
            )
            
            # 결과 파싱
            results = []
            for match in search_response.matches:
                # 점수 필터링
                if match.score < score_threshold:
                    continue
                
                metadata = match.metadata or {}
                result = SearchResult(
                    id=match.id,
                    score=match.score,
                    source_type=metadata.get("source_type", "unknown"),
                    title=metadata.get("title", ""),
                    content=metadata.get("content", "")
                )
                results.append(result)
            
            print(f"🔍 검색 완료: {len(results)}개 결과 (임계값: {score_threshold})")
            return results
            
        except Exception as e:
            print(f"❌ Pinecone 검색 실패: {e}")
            return []
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        score_threshold: float = 0.7,
        source_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """
        통합 검색 함수 (임베딩 + 벡터검색)
        
        Args:
            query: 사용자 질문
            top_k: 반환할 결과 수  
            score_threshold: 최소 유사도 점수
            source_filter: 소스 타입 필터
            
        Returns:
            검색 결과 리스트
        """
        print(f"🔍 검색 시작: '{query}'")
        
        # 1. 질문 임베딩
        try:
            query_vector = self.embed_query(query)
            print(f"✅ 임베딩 완료 (차원: {len(query_vector)})")
        except Exception as e:
            print(f"❌ 임베딩 실패: {e}")
            return []
        
        # 2. 벡터 검색
        results = self.search_similar(
            query_vector, 
            top_k=top_k,
            score_threshold=score_threshold,
            source_filter=source_filter
        )
        
        return results
    
    def build_context(
        self, 
        search_results: List[SearchResult],
        max_length: int = 2000
    ) -> str:
        """
        검색 결과를 OpenAI용 컨텍스트로 구성
        
        Args:
            search_results: 검색 결과
            max_length: 최대 컨텍스트 길이
            
        Returns:
            구조화된 컨텍스트 문자열
        """
        if not search_results:
            return "관련 정보를 찾을 수 없습니다."
        
        context_parts = []
        current_length = 0
        
        for i, result in enumerate(search_results, 1):
            # 소스별 아이콘
            icon_map = {
                "contacts": "📞",
                "news": "📰", 
                "guide": "📋",
                "terms": "📚",
                "insurance": "🛡️"
            }
            icon = icon_map.get(result.source_type, "📄")
            
            # 컨텍스트 항목 구성
            item = f"""{icon} **{result.title}** (신뢰도: {result.score:.2f})
{result.content}

"""
            
            # 길이 체크
            if current_length + len(item) > max_length:
                break
                
            context_parts.append(item)
            current_length += len(item)
        
        context = "## 📋 관련 정보\n\n" + "".join(context_parts)
        
        # 소스 요약
        source_summary = {}
        for result in search_results[:len(context_parts)]:
            source_type = result.source_type
            source_summary[source_type] = source_summary.get(source_type, 0) + 1
        
        summary = ", ".join([f"{k}({v}개)" for k, v in source_summary.items()])
        context += f"\n*💡 총 {len(context_parts)}개 자료 활용: {summary}*"
        
        return context
    
    def search_and_build_context(
        self, 
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.7,
        max_context_length: int = 2000,
        source_filter: Optional[str] = None
    ) -> Tuple[List[SearchResult], str]:
        """
        검색부터 컨텍스트 구성까지 원스톱 함수
        
        Returns:
            (검색결과, 컨텍스트)
        """
        # 검색
        results = self.search(
            query=query,
            top_k=top_k, 
            score_threshold=score_threshold,
            source_filter=source_filter
        )
        
        # 컨텍스트 구성
        context = self.build_context(results, max_context_length)
        
        return results, context


# 사용 예시 및 테스트
def main():
    """테스트 함수"""
    # 검색 엔진 초기화
    rag = RAGSearchEngine()
    
    # 테스트 질문들
    test_queries = [
        "메리츠화재 연락처가 궁금해요",
        "자동차 사고 신고는 어떻게 하나요?",
        "보험료 할인 방법 알려주세요",
        "과실비율은 어떻게 정해지나요?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 테스트 질문: {query}")
        print('='*60)
        
        # 검색 및 컨텍스트 구성
        results, context = rag.search_and_build_context(
            query=query,
            top_k=3,
            score_threshold=0.6
        )
        
        # 결과 출력
        print(f"\n📊 검색 결과 ({len(results)}개):")
        for result in results:
            print(f"  • {result.title} ({result.score:.3f}) - {result.source_type}")
        
        print(f"\n📋 생성된 컨텍스트:")
        print(context)
        
        print(f"\n💬 컨텍스트 길이: {len(context)} 문자")


if __name__ == "__main__":
    main()