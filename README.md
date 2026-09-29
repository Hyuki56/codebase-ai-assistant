codebase-ai-assistant/
│
├── app.py                 # 프로그램 시작
│
├── loader/
│   └── github_loader.py   # Repository 읽기 
                            from pathlib import Path를 통해
├── chunker/
│   └── code_chunker.py    # 코드 분할
│
├── embedding/
│   └── embedder.py        # 임베딩 생성
│
├── vectorstore/
│   └── chroma_store.py    # ChromaDB 저장
│
├── rag/
│   ├── retriever.py       # 검색
│   └── prompt.py          # 프롬프트
│
├── llm/
│   └── ollama_client.py   # Ollama 호출
│
├── api/
│   └── api.py             # FastAPI
│
├── data/
│
├── requirements.txt
│
└── README.md



라이브러리	역할
ollama	/ 로컬 LLM 호출
chromadb / 벡터 데이터베이스
sentence-transformers / 코드/문서를 벡터로 변환(Embedding)
fastapi	/ API 서버
uvicorn	/ FastAPI 실행

## PJ1 서비스화 - 1단계

### 실행

프로젝트 루트에서:

```bash
uvicorn api.api:app --reload
```

서버가 실행되면:

- `GET /health` : 서버 상태 확인
- `POST /api/index` : 로컬 Python Repository를 분석하고 ChromaDB에 색인
- `POST /api/ask` : 색인된 코드에 질문

FastAPI 기본 문서는:

```text
http://127.0.0.1:8000/docs
```

### 요청 예시

`/api/index`

```json
{
  "repo_path": "../AI-Smart-Surveillance-Platform"
}
```

`/api/ask`

```json
{
  "question": "ZoneManager에서 제한구역 진입 여부는 어떻게 판단하나요?"
}
```
