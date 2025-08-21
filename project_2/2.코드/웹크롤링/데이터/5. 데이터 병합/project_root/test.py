import os
from dotenv import load_dotenv
from rag_search import RAGSearchEngine

# 초기화
rag = RAGSearchEngine()

# 검색
results, context = rag.search_and_build_context(
    query="메리츠화재 연락처",
    top_k=3,
    score_threshold=0.7
)

print(context)  # OpenAI로 전달할 컨텍스트

print(load_dotenv())
print("UPSTAGE_API_KEY:", os.getenv("UPSTAGE_API_KEY"))
print("PINECONE_API_KEY:", os.getenv("PINECONE_API_KEY"))