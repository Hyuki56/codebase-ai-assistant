import chromadb


class ChromaManager:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./database"
        )


    def load(self):
        self.collection = self.client.get_or_create_collection(
            name="code_chunks"
        )


    def reset(self):

        try:
            self.client.delete_collection(
                name="code_chunks"
            )

        except Exception:
            pass


        self.collection = self.client.get_or_create_collection(
            name="code_chunks"
        )


    def add_chunk(
        self,
        chunk_id,
        text,
        embedding,
        path,
        chunk_type,
        chunk_name
    ):

        self.collection.add(

            ids=[chunk_id],

            documents=[text],

            embeddings=[embedding],

            metadatas=[
                {
                    "path": path,
                    "chunk_type": chunk_type,
                    "chunk_name": chunk_name
                }
            ]

        )

        print(
            f"저장 완료: "
            f"{chunk_type} {chunk_name}"
        )


    def search(self, query_embedding):

        results = self.collection.query(

            query_embeddings=[query_embedding],

            n_results=5

        )


        return (

            results["documents"][0],

            results["metadatas"][0]

        )