from loader.github_loader import GitHubLoader
from chunker.code_chunker import CodeChunker
from embedding.embedder import Embedder
from vectordb.chroma_manager import ChromaManager

def main():
    repo = GitHubLoader("../AI-Smart-Surveillance-Platform")
    files = repo.load_python_files()

    chunker = CodeChunker()
    embedder = Embedder()
    db = ChromaManager()
    db.reset()

    chunk_id = 1

    for file in files:
        chunks = chunker.chunk(file['content'])

        for chunk in chunks:
            vector = embedder.embed(chunk)

            db.add_chunk(
                chunk_id=f'chunk_{chunk_id}',
                text=chunk,
                embedding=vector,
                path=file['path']
            )
            chunk_id += 1

    print("=" * 50)
    print(f"총 저장된 Chunk : {chunk_id - 1}")
    print("=" * 50)

if __name__ == "__main__":
    main()