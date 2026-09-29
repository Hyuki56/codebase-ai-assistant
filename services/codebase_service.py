from chunker.code_chunker import CodeChunker
from embedding.embedder import Embedder
from llm.ollama_client import OllamaClient
from loader.github_loader import GitHubLoader
from vectordb.chroma_manager import ChromaManager


class CodebaseService:

    def __init__(self):
        self.chunker = CodeChunker()
        self.embedder = Embedder()
        self.db = ChromaManager()
        self.client = OllamaClient()

        self.db.load()


    def index_repository(self, repo_path: str) -> dict:

        repo = GitHubLoader(repo_path)

        files = repo.load_python_files()

        if not files:
            raise ValueError(
                "Python 파일을 찾지 못했습니다."
            )


        self.db.reset()


        chunk_count = 0


        for file in files:

            chunks = self.chunker.chunk(
                file["content"]
            )


            for chunk in chunks:

                text = chunk["text"]

                vector = self.embedder.embed(
                    text
                )


                self.db.add_chunk(

                    chunk_id=f"chunk_{chunk_count + 1}",

                    text=text,

                    embedding=vector,

                    path=file["path"],

                    chunk_type=chunk["type"],

                    chunk_name=chunk["name"]

                )


                chunk_count += 1


        return {

            "repo_path": repo_path,

            "file_count": len(files),

            "chunk_count": chunk_count

        }


    def ask(self, question: str) -> dict:

        if not question.strip():

            raise ValueError(
                "질문을 입력해주세요."
            )


        query_vector = self.embedder.embed(
            question
        )


        documents, metadatas = self.db.search(
            query_vector
        )


        contexts = []


        for doc, meta in zip(
            documents,
            metadatas
        ):

            contexts.append(

                f"파일: {meta['path']}\n"
                f"구조: {meta['chunk_type']} "
                f"{meta['chunk_name']}\n"
                f"코드:\n{doc}"

            )


        context = "\n\n".join(
            contexts
        )


        answer = self.client.ask(
            question,
            context
        )


        return {

            "question": question,

            "answer": answer,

            "sources": [
                meta["path"]
                for meta in metadatas
            ]

        }