# Codebase AI Assistant (PJ1)

로컬 Python 소스코드 리포지토리를 인덱싱하고, RAG(Retrieval-Augmented Generation) 파이프라인과 로컬 LLM을 활용해 코드 구조와 로직에 대한 질의응답을 제공하는 AI 어시스턴트 서비스입니다.

사용자가 지정한 로컬 Python 리포지토리에서 소스코드를 읽고 코드 조각을 분할합니다. Ollama의 `nomic-embed-text` 모델로 임베딩을 생성해 ChromaDB에 저장하고, 질문이 들어오면 관련 코드 조각을 검색하여 로컬 LLM이 답변을 생성합니다.

## 주요 기능

- Python 코드 로딩: 지정한 로컬 리포지토리에서 Python 소스코드 로드
- 코드 청킹: 소스코드를 검색에 활용할 수 있는 단위로 분할
- 임베딩 생성: Ollama의 `nomic-embed-text` 모델로 코드와 질문을 벡터로 변환
- 벡터 저장 및 검색: ChromaDB에 코드 임베딩을 저장하고 관련 코드 검색
- RAG 기반 질의응답: 검색된 코드 컨텍스트를 활용해 로컬 LLM 답변 생성
- REST API: FastAPI를 통한 코드 인덱싱 및 질의응답 API 제공
- 웹 인터페이스: HTML 템플릿과 CSS를 활용한 브라우저 화면 제공

## 시스템 아키텍처

### 인덱싱 흐름

`Python Repository → Repository Loader → Code Chunker → Ollama Embedding → ChromaDB`

### 질의응답 흐름

`사용자 질문 → 질문 임베딩 → ChromaDB 관련 코드 검색 → 컨텍스트 구성 → Ollama LLM → 답변 반환`

FastAPI는 인덱싱 및 질의응답 기능을 API로 제공하며, HTML 템플릿과 CSS를 통해 웹 화면을 제공합니다.

## 기술 스택

| 기술 | 역할 |
|---|---|
| Python | 서비스 및 RAG 파이프라인 구현 |
| FastAPI | REST API 및 웹 요청 처리 |
| Uvicorn | FastAPI 서버 실행 |
| Ollama | 로컬 임베딩 및 LLM 모델 호출 |
| `nomic-embed-text` | 코드와 질문의 임베딩 벡터 생성 |
| `qwen2.5-coder:7b` | 코드 관련 질문에 대한 답변 생성 |
| ChromaDB | 코드 임베딩 저장 및 유사도 검색 |
| HTML / CSS | 웹 인터페이스 구성 |
| `requests` | Ollama API HTTP 요청 |

## 프로젝트 구조

```text
codebase-ai-assistant-pj1-service-step1/
├── api/
│   └── api.py
├── chunker/
│   └── code_chunker.py
├── database/
├── embedding/
│   └── embedder.py
├── llm/
│   └── ollama_client.py
├── loader/
│   └── github_loader.py
├── services/
│   └── codebase_service.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── test_database/
├── vectordb/
│   └── chroma_manager.py
├── app.py
├── index.py
├── requirements.txt
└── README.md
```

- `api/`: FastAPI 엔드포인트와 웹 요청 처리
- `chunker/`: 소스코드 분할
- `database/`: 데이터베이스 관련 경로
- `embedding/`: Ollama 임베딩 API를 통한 벡터 생성
- `llm/`: Ollama LLM 클라이언트
- `loader/`: 로컬 Python 리포지토리 로딩
- `services/`: 인덱싱 및 질의응답 처리 흐름 관리
- `static/`: CSS 정적 파일
- `templates/`: HTML 웹 화면
- `test_database/`: 테스트용 데이터베이스 경로
- `vectordb/`: ChromaDB 연동
- `app.py`: 콘솔 기반 질의응답 스크립트
- `index.py`: 대상 리포지토리 코드 인덱싱 스크립트

## 실행 방법

### 1. 사전 준비

- Python 설치
- Ollama 설치 및 실행
- 임베딩 모델 및 질의응답 모델 다운로드

이 프로젝트는 Python 3.11 환경을 권장합니다. 다만, 테스트용 복제본에서는 Python 3.13.9 환경에서도 의존성 설치와 주요 RAG 기능의 동작을 확인했습니다.

Ollama에서 다음 모델을 준비합니다.

```powershell
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:7b
```

모델 다운로드 후 Ollama가 실행 중인지 확인합니다.

```powershell
ollama list
```

### 2. 가상환경 생성 및 의존성 설치

프로젝트 루트에서 실행합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

PowerShell 실행 정책으로 가상환경 활성화가 제한되는 경우에도 위와 같이 가상환경의 Python 실행 파일을 직접 사용하면 됩니다.

### 3. FastAPI 서버 실행

프로젝트 루트에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.api:app --host 127.0.0.1 --port 8000 --reload
```

### 4. 서비스 접속

- 웹 화면: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- API 문서: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 서버 상태 확인: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 5. 코드 인덱싱 및 질의응답

먼저 웹 화면 또는 API를 통해 대상 Python 리포지토리를 인덱싱합니다.

`POST /api/index` 요청 예시:

```json
{
  "repo_path": "../AI-Smart-Surveillance-Platform"
}
```

`repo_path`에는 실제 대상 리포지토리의 로컬 경로를 입력합니다. 상대 경로를 사용할 경우 기준 경로가 코드에서 어떻게 처리되는지 확인하고, 필요하면 절대 경로를 사용합니다.

인덱싱이 완료되면 `POST /api/ask`로 질문할 수 있습니다.

```json
{
  "question": "ZoneManager에서 제한구역 진입 여부는 어떻게 판단하나요?"
}
```

응답에는 질문에 대한 생성 답변과 검색된 소스 파일 경로 등이 포함됩니다.

## API

### `GET /health`

서버 상태를 확인합니다.

응답 예시:

```json
{
  "status": "ok"
}
```

### `POST /api/index`

지정한 로컬 Python 리포지토리를 읽고 코드 청킹 및 벡터 인덱싱을 수행합니다.

요청 본문에 `repo_path`를 지정합니다. 처리 결과에는 리포지토리 경로, 처리 파일 수, 청크 수 등이 포함됩니다.

### `POST /api/ask`

인덱싱된 코드에서 질문과 관련된 컨텍스트를 검색하고 LLM 답변을 생성합니다.

요청 본문에 `question`을 지정합니다. 응답에는 생성 답변과 검색된 소스 파일 경로 등이 포함됩니다.

## 프로젝트를 통해 구현한 내용

- 로컬 Python 리포지토리 로딩부터 코드 청킹, 임베딩, 벡터 검색까지 이어지는 처리 흐름 구현
- ChromaDB를 이용한 코드 임베딩 저장 및 검색
- 검색 결과를 컨텍스트로 활용하는 RAG 기반 질의응답
- Ollama 로컬 모델과 FastAPI를 연결한 서비스 API
- HTML/CSS 기반 웹 인터페이스 제공

## 향후 개선 방향

- 다양한 Python 리포지토리를 대상으로 검색 품질 검증
- 검색 결과 및 답변 품질 평가
- 인덱싱 시간과 응답 속도 측정 및 개선
- 오류 처리와 자동화 테스트 범위 확장
