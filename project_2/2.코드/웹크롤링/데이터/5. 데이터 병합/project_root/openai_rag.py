# -*- coding: utf-8 -*-
"""
OpenAI + RAG 통합 시스템
검색된 컨텍스트를 바탕으로 OpenAI가 예쁜 답변 생성
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass

import openai
from dotenv import load_dotenv
from rag_search import RAGSearchEngine, SearchResult

load_dotenv()

@dataclass
class ChatResponse:
    """챗봇 응답 데이터 클래스"""
    answer: str
    sources: List[SearchResult]
    search_query: str
    model_used: str
    context_length: int

class OpenAIRAGSystem:
    """OpenAI + RAG 통합 시스템"""
    
    def __init__(self):
        # 환경변수 로드
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # 검증
        assert self.openai_api_key, "OPENAI_API_KEY가 필요합니다"
        
        # OpenAI 클라이언트 초기화
        openai.api_key = self.openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # RAG 검색 엔진 초기화
        self.rag_engine = RAGSearchEngine()
        
        print(f"✅ OpenAI RAG 시스템 초기화 완료")
        print(f"   OpenAI 모델: {self.openai_model}")
    
    def create_system_prompt(self) -> str:
        """시스템 프롬프트 생성"""
        return """당신은 자동차보험 전문 상담사입니다. 

## 역할
- 사용자의 자동차보험 관련 질문에 친절하고 정확하게 답변
- 제공된 검색 결과를 바탕으로 신뢰할 수 있는 정보 제공
- 복잡한 보험 용어를 쉽게 설명

## 답변 규칙
1. **친근하고 전문적인 톤**: 존댓말 사용, 이해하기 쉽게 설명
2. **구조화된 답변**: 단계별, 항목별로 정리
3. **출처 명시**: 답변 근거가 되는 정보의 출처 표시
4. **실용적 조언**: 구체적이고 실행 가능한 가이드 제공
5. **추가 도움**: 관련 질문이나 추가 정보 제안

## 답변 형식
```
🎯 **핵심 답변**
[질문에 대한 직접적인 답변]

📋 **상세 정보**
- 항목 1: 설명
- 항목 2: 설명

💡 **추가 팁**
[유용한 추가 정보나 주의사항]

📞 **관련 연락처** (해당시)
[보험사 연락처 등]
```

## 제한사항
- 검색 결과에 없는 정보는 추측하지 말고 "추가 확인이 필요하다"고 안내
- 법적 조언이나 확정적인 보험료는 제공하지 말고 전문가 상담 권유
- 개인정보는 절대 요구하지 않음"""

    def create_user_prompt(self, query: str, context: str) -> str:
        """사용자 프롬프트 생성"""
        return f"""사용자 질문: {query}

## 검색된 관련 정보:
{context}

위 정보를 바탕으로 사용자의 질문에 정확하고 친절하게 답변해주세요.
검색 결과에 관련 정보가 부족하다면, 일반적인 가이드라인을 제공하되 "정확한 정보는 해당 보험사에 문의"라고 안내해주세요."""

    def generate_answer(
        self, 
        query: str, 
        context: str,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> str:
        """
        OpenAI로 답변 생성
        
        Args:
            query: 사용자 질문
            context: 검색된 컨텍스트
            temperature: 창의성 수준 (0.0-1.0)
            max_tokens: 최대 토큰 수
            
        Returns:
            생성된 답변
        """
        try:
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": self.create_user_prompt(query, context)}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ OpenAI API 오류: {e}")
            return f"죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.\n\n📋 검색된 정보:\n{context}"

    def chat(
        self, 
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.6,
        source_filter: Optional[str] = None
    ) -> ChatResponse:
        """
        통합 채팅 함수 (검색 + 생성)
        
        Args:
            query: 사용자 질문
            top_k: 검색할 결과 수
            score_threshold: 검색 점수 임계값
            source_filter: 소스 타입 필터
            
        Returns:
            ChatResponse 객체
        """
        print(f"💬 사용자 질문: '{query}'")
        
        # 1. RAG 검색
        search_results, context = self.rag_engine.search_and_build_context(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            source_filter=source_filter
        )
        
        print(f"🔍 검색 완료: {len(search_results)}개 결과")
        
        # 2. OpenAI로 답변 생성
        print(f"🤖 답변 생성 중...")
        answer = self.generate_answer(query, context)
        
        # 3. 응답 구성
        response = ChatResponse(
            answer=answer,
            sources=search_results,
            search_query=query,
            model_used=self.openai_model,
            context_length=len(context)
        )
        
        print(f"✅ 답변 생성 완료 (길이: {len(answer)} 문자)")
        return response

    def print_response(self, response: ChatResponse):
        """응답을 예쁘게 출력"""
        print("\n" + "="*80)
        print("🤖 AI 상담사 답변")
        print("="*80)
        print(response.answer)
        
        print(f"\n📊 **메타 정보**")
        print(f"   • 검색 결과: {len(response.sources)}개")
        print(f"   • 사용 모델: {response.model_used}")
        print(f"   • 컨텍스트 길이: {response.context_length} 문자")
        
        if response.sources:
            print(f"\n📚 **참조한 자료**:")
            for i, source in enumerate(response.sources, 1):
                print(f"   {i}. {source.title} ({source.score:.3f}) - {source.source_type}")


# 테스트 함수
def main():
    """OpenAI RAG 시스템 테스트"""
    
    # 시스템 초기화
    rag_chat = OpenAIRAGSystem()
    
    # 테스트 질문들
    test_questions = [
        "메리츠화재 연락처를 알려주세요",
        "자동차 사고가 났을 때 어떻게 해야 하나요?",
        "대인배상보험이 뭔가요?",
        "보험료를 절약할 수 있는 방법이 있을까요?",
        "전기차 보험료 혜택에 대해 알려주세요"
    ]
    
    for question in test_questions:
        print(f"\n{'🔸'*50}")
        
        # 채팅 실행
        response = rag_chat.chat(question)
        
        # 결과 출력
        rag_chat.print_response(response)
        
        # 구분선
        print("\n" + "⏸️ "*25)
        input("Enter를 눌러서 다음 질문으로...")

if __name__ == "__main__":
    main()