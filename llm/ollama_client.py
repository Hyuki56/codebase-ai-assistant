import requests


class OllamaClient:

    def __init__(self):
        self.model = "qwen2.5-coder:7b"
        self.url = "http://127.0.0.1:11434/api/generate"


    def ask(self, question, context):

        prompt = f"""
당신은 Python 프로젝트의 코드를 분석하는 AI Assistant입니다.

반드시 아래 규칙을 지키세요.

1. 반드시 한국어로 답변하세요.
2. 제공된 [Code Context]만 근거로 답변하세요.
3. 추측하거나 코드에 없는 내용을 만들어내지 마세요.
4. 답변에 반드시 파일 경로를 포함하세요.
5. 가능하면 클래스명 또는 함수명을 함께 표시하세요.
6. 질문과 직접적으로 관련된 코드만 중심적으로 설명하세요.
7. 검색된 코드가 질문과 직접적으로 관련되지 않는다면
   "제공된 검색 결과에서는 정확한 위치를 확인하기 어렵습니다."
   라고 답변하세요.
8. 코드가 질문에 대한 근거가 되는 경우 핵심 코드를 함께 설명하세요.
9. 서로 다른 파일에 비슷한 코드가 있다면 각각의 역할을 구분해서 설명하세요.
10. `auto_label.py`처럼 데이터 준비나 자동 라벨링을 위한 코드와
    실제 애플리케이션에서 객체 탐지를 수행하는 코드를 구분해서 설명하세요.

[Code Context]

{context}


[Question]

{question}


[Answer]

위 규칙을 지키면서 질문에 답변하세요.
"""


        response = requests.post(

            self.url,

            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },

            timeout=300

        )


        response.raise_for_status()


        data = response.json()


        if "response" not in data:

            raise ValueError(
                f"Ollama 응답에서 response를 찾을 수 없습니다: {data}"
            )


        return data["response"]