from pathlib import Path

IGNORE_DIRS = {
    ".git",
    ".github",
    ".idea",
    "venv",
    ".venv",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules"
}

class GitHubLoader:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)

    def load_python_files(self):
        files = []
        for file in self.repo_path.rglob("*.py"):
            if any(ignore in file.parts for ignore in IGNORE_DIRS):
                continue

            try:
                content = file.read_text(
                    encoding="utf-8"
                )

            except UnicodeDecodeError:
                continue

            files.append({
                "path": str(file),
                "content": content
            })

        return files