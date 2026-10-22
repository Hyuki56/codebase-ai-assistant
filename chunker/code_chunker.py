import ast


class CodeChunker:
    MAX_CHARS = 1500  # Ollama 컨텍스트 한도를 안전하게 방어하기 위한 글자 수 제한

    def chunk(self, text):
        chunks = []

        try:
            tree = ast.parse(text)
        except SyntaxError:
            # 문법 오류가 난 파일은 안전하게 MAX_CHARS 단위로 쪼갬
            return self._split_text(text, chunk_type="module", name="unknown")

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                source = ast.get_source_segment(text, node)
                if source:
                    chunks.extend(self._safe_split(source, "class", node.name))

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                source = ast.get_source_segment(text, node)
                if source:
                    chunks.extend(self._safe_split(source, "function", node.name))

        # 클래스나 함수가 하나도 없는 파일인 경우
        if not chunks:
            chunks.extend(self._safe_split(text, "module", "module"))

        return chunks

    def _safe_split(self, source, chunk_type, name):
        """지정된 최대 글자 수(MAX_CHARS)를 넘지 않도록 안전하게 분할하는 메서드"""
        if not source.strip():
            return []

        if len(source) <= self.MAX_CHARS:
            return [{
                "text": source,
                "type": chunk_type,
                "name": name
            }]

        # 코드가 너무 길면 줄바꿈 기준으로 자연스럽게 쪼갬
        lines = source.splitlines()
        chunks = []
        current_lines = []
        current_len = 0
        part = 1

        for line in lines:
            line_len = len(line) + 1  # newline 포함
            if current_len + line_len > self.MAX_CHARS and current_lines:
                chunks.append({
                    "text": "\n".join(current_lines),
                    "type": chunk_type,
                    "name": f"{name}_part{part}"
                })
                part += 1
                current_lines = [line]
                current_len = line_len
            else:
                current_lines.append(line)
                current_len += line_len

        if current_lines:
            chunks.append({
                "text": "\n".join(current_lines),
                "type": chunk_type,
                "name": f"{name}_part{part}" if part > 1 else name
            })

        return chunks

    def _split_text(self, text, chunk_type, name):
        return self._safe_split(text, chunk_type, name)