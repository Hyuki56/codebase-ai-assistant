from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.codebase_service import CodebaseService


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(
    title="Codebase AI Assistant",
    description="RAG 기반 Python 코드 분석 API",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


class IndexRequest(BaseModel):
    repo_path: str


class AskRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():
    html_path = BASE_DIR / "templates" / "index.html"

    return html_path.read_text(
        encoding="utf-8"
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/index")
def index_repository(request: IndexRequest):
    try:
        service = CodebaseService()

        return service.index_repository(
            request.repo_path
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/api/ask")
def ask(request: AskRequest):
    try:
        service = CodebaseService()

        return service.ask(
            request.question
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )