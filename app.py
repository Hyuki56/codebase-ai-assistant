from embedding.embedder import Embedder
from vectordb.chroma_manager import ChromaManager
from llm.ollama_client import OllamaClient

def main():
    embedder = Embedder()
    db = ChromaManager()
    client = OllamaClient()
    db.load()

    while True:
        question = input("Question :")

        if question.lower() == "exit":
            break

        query_vector = embedder.embed(question)

        documents, metadatas = db.search(query_vector)
        contexts = []
        for doc, meta in zip(documents, metadatas):
            contexts.append(
                f"""
                    \n파일:{meta['path']}
                    \n코드:{doc}
                """
            )

        context = "\n\n".join(contexts)
        print("=" * 50)
        print(context)
        print("=" * 50)

        answer = client.ask(question, context)
        print("\nAnswer")
        print(answer)


if __name__ == "__main__":
    main()