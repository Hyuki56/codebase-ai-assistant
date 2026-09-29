import ast


class CodeChunker:

    def chunk(self, text):
        chunks = []

        try:
            tree = ast.parse(text)

        except SyntaxError:
            return [
                {
                    "text": text,
                    "type": "module",
                    "name": "unknown"
                }
            ]

        for node in tree.body:

            if isinstance(node, ast.ClassDef):

                chunk = ast.get_source_segment(
                    text,
                    node
                )

                if chunk:
                    chunks.append(
                        {
                            "text": chunk,
                            "type": "class",
                            "name": node.name
                        }
                    )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                chunk = ast.get_source_segment(
                    text,
                    node
                )

                if chunk:
                    chunks.append(
                        {
                            "text": chunk,
                            "type": "function",
                            "name": node.name
                        }
                    )

        if not chunks:

            chunks.append(
                {
                    "text": text,
                    "type": "module",
                    "name": "module"
                }
            )

        return chunks