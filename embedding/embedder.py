
import requests


class Embedder:
    def __init__(self):
        self.model = "nomic-embed-text"
        self.url = "http://127.0.0.1:11434/api/embeddings"

    def embed(self, text):
        if not text or not text.strip():
            return [0.0] * 768

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": text,
                },
                timeout=120,
            )
            response.raise_for_status()

        except requests.RequestException as e:
            print("Ollama 임베딩 요청 실패")
            print(f"모델: {self.model}")
            print(f"입력 길이: {len(text)}")
            print(f"오류: {e}")

            if e.response is not None:
                print(f"응답 본문: {e.response.text}")

            raise

        data = response.json()
        embedding = data.get("embedding")

        if not isinstance(embedding, list) or not embedding:
            raise ValueError(
                f"올바르지 않은 임베딩 응답: {data}"
            )

        if not all(
            isinstance(value, (int, float))
            for value in embedding
        ):
            raise ValueError(
                f"임베딩에 숫자가 아닌 값이 있습니다: "
                f"{embedding[:5]}"
            )

        print(f"임베딩 생성 성공: 차원={len(embedding)}")

        return embedding
