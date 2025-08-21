# -*- coding: utf-8 -*-
"""
out/corpus.jsonl → Upstage 임베딩 → Pinecone 업서트 (수정된 버전)

환경변수 필수:
- UPSTAGE_API_KEY
- PINECONE_API_KEY
"""

import os
import json
import time
from pathlib import Path

import requests
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()

CORPUS_PATH = Path("./out/corpus.jsonl")

UPSTAGE_API_KEY   = os.getenv("UPSTAGE_API_KEY")
UPSTAGE_EMBED_URL = os.getenv("UPSTAGE_EMBED_URL", "https://api.upstage.ai/v1/embeddings")
UPSTAGE_MODEL     = "solar-embedding-1-large-query"  # 🔧 passage → query로 변경

PINECONE_API_KEY  = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = "insurance-documents"
PINECONE_REGION = "us-east-1"
PINECONE_CLOUD = "aws"
NAMESPACE = "insurance-hub"

BATCH_SIZE = 32  # 🔧 배치 사이즈 줄임 (안정성)
RETRY_WAIT = 3

def upstage_embed(texts):
    """
    Upstage 임베딩 호출. 429 등 에러 시 재시도.
    반환: list[list[float]]
    """
    headers = {"Authorization": f"Bearer {UPSTAGE_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": UPSTAGE_MODEL, "input": texts}
    
    for attempt in range(5):
        try:
            r = requests.post(UPSTAGE_EMBED_URL, headers=headers, json=payload, timeout=60)
            if r.status_code == 200:
                data = r.json()
                # 🔧 모든 벡터 값을 float로 변환
                embeddings = []
                for item in data["data"]:
                    embedding = [float(x) for x in item["embedding"]]  # int → float 변환
                    embeddings.append(embedding)
                return embeddings
            else:
                # 디버그 출력
                print(f"[Upstage {attempt+1}/5] status={r.status_code}")
                print(f"Response: {r.text[:400]}")
                
        except Exception as e:
            print(f"[Upstage {attempt+1}/5] Exception: {e}")
            
        time.sleep(RETRY_WAIT * (attempt + 1))
    
    raise Exception(f"Failed to embed after 5 attempts")

def ensure_index(pc: Pinecone, index_name: str, dim: int):
    """인덱스 생성 또는 확인"""
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name in existing_indexes:
        print(f"✅ 인덱스 '{index_name}' 이미 존재")
        return
    
    print(f"🔨 인덱스 '{index_name}' 생성 중... (차원: {dim})")
    pc.create_index(
        name=index_name,
        dimension=dim,
        metric="cosine",
        spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
    )
    
    # 인덱스 생성 대기
    print("⏳ 인덱스 초기화 대기 중...")
    time.sleep(10)
    print("✅ 인덱스 생성 완료")

def batched(xs, n=BATCH_SIZE):
    """리스트를 배치로 나누기"""
    batch = []
    for x in xs:
        batch.append(x)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch

def validate_corpus(corpus_path):
    """코퍼스 파일 검증"""
    if not corpus_path.exists():
        print(f"❌ 코퍼스 파일이 없습니다: {corpus_path}")
        print("   경로를 확인하거나 데이터 전처리를 먼저 실행하세요.")
        return False
    
    # 샘플 확인
    with open(corpus_path, encoding="utf-8") as f:
        first_line = f.readline()
        try:
            sample = json.loads(first_line)
            required_fields = ["id", "content"]
            missing = [field for field in required_fields if field not in sample]
            if missing:
                print(f"❌ 필수 필드 누락: {missing}")
                return False
            print(f"✅ 코퍼스 파일 검증 완료")
            print(f"   샘플: {sample}")
            return True
        except json.JSONDecodeError:
            print(f"❌ JSON 형식 오류")
            return False

def main():
    print("🚀 Pinecone 업로드 시작")
    print("=" * 50)
    
    # 1. 환경 검증
    assert UPSTAGE_API_KEY, "❌ UPSTAGE_API_KEY is required"
    assert PINECONE_API_KEY, "❌ PINECONE_API_KEY is required"
    
    print(f"📋 설정:")
    print(f"   코퍼스: {CORPUS_PATH}")
    print(f"   Upstage 모델: {UPSTAGE_MODEL}")
    print(f"   Pinecone 인덱스: {PINECONE_INDEX}")
    print(f"   네임스페이스: {NAMESPACE}")
    
    # 2. 코퍼스 검증
    if not validate_corpus(CORPUS_PATH):
        return
    
    # 3. 데이터 로드
    print(f"\n📚 데이터 로딩...")
    items = []
    with open(CORPUS_PATH, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                item = json.loads(line)
                items.append(item)
            except json.JSONDecodeError as e:
                print(f"⚠️  라인 {line_num} 스킵 (JSON 오류): {e}")
    
    print(f"✅ {len(items)}개 아이템 로드 완료")
    if not items:
        print("❌ 업로드할 데이터가 없습니다")
        return

    # 4. 첫 배치로 차원 확인
    print(f"\n🔍 임베딩 차원 확인...")
    probe_texts = [item["content"] for item in items[:min(4, len(items))]]
    probe_vecs = upstage_embed(probe_texts)
    dim = len(probe_vecs[0])
    print(f"✅ 임베딩 차원: {dim}")

    # 5. Pinecone 초기화
    print(f"\n🔗 Pinecone 연결...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    ensure_index(pc, PINECONE_INDEX, dim)
    index = pc.Index(PINECONE_INDEX)

    # 6. 업서트 실행
    print(f"\n📤 벡터 업로드 중...")
    total_uploaded = 0
    failed_batches = 0
    
    for batch_num, batch in enumerate(tqdm(batched(items), 
                                          total=(len(items)+BATCH_SIZE-1)//BATCH_SIZE, 
                                          desc="업로드")):
        try:
            # 임베딩
            texts = [item["content"] for item in batch]
            vecs = upstage_embed(texts)
            
            # 업서트 데이터 구성
            to_upsert = []
            for item, vec in zip(batch, vecs):
                # 🔧 벡터 타입 검증 및 변환
                safe_vector = [float(x) for x in vec]  # 추가 안전장치
                
                to_upsert.append({
                    "id": item["id"],
                    "values": safe_vector,  # float 보장된 벡터
                    "metadata": {
                        "source_type": item.get("source_type", "unknown"),
                        "title": item.get("title", ""),
                        "content": item.get("content", "")[:1000],  # 메타데이터 크기 제한
                    }
                })
            
            # Pinecone 업서트
            index.upsert(vectors=to_upsert, namespace=NAMESPACE)
            total_uploaded += len(to_upsert)
            
        except Exception as e:
            failed_batches += 1
            print(f"\n❌ 배치 {batch_num+1} 실패: {e}")
            
            # 3회 연속 실패시 중단
            if failed_batches >= 3:
                print("❌ 연속 실패로 업로드 중단")
                break

    # 7. 결과 확인
    print(f"\n" + "=" * 50)
    print(f"📊 업로드 완료!")
    print(f"   성공: {total_uploaded}개 벡터")
    print(f"   실패: {failed_batches}개 배치")
    print(f"   인덱스: {PINECONE_INDEX}")
    print(f"   네임스페이스: {NAMESPACE}")
    
    # 인덱스 통계 확인
    time.sleep(5)  # 업데이트 대기
    try:
        stats = index.describe_index_stats()
        print(f"   확인된 벡터 수: {stats.total_vector_count}")
        print(f"   네임스페이스별: {stats.namespaces}")
    except Exception as e:
        print(f"   통계 확인 실패: {e}")

if __name__ == "__main__":
    main()