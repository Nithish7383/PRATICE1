class OllamaLLM:
    def __init__(self, model="mistral"):
        self.model = model
        self._ollama = None

    def _load_ollama(self):
        if self._ollama is None:
            try:
                import ollama
                self._ollama = ollama
            except ImportError:
                return None
        return self._ollama

    def generate(self, prompt: str) -> str:
        ollama = self._load_ollama()

        if ollama is None:
            return (
                "AI explanation unavailable. "
                "Release risk score shown is deterministic and validated."
            )

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
