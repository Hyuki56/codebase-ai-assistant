import requests


class Embedder:
    def __init__(self):
        self.model = "nomic-embed-text"
        self.url = "http://127.0.0.1:11434/api/embeddings"

    def embed(self, text):
        if not text or not text.strip():
            return [0.0] * 768

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": text,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        if "embedding" not in data:
            raise ValueError(
                f"Ollama 응답에서 embedding을 찾을 수 없습니다: {data}"
            )

        return data["embedding"]