import ollama

class OllamaLLM:
    def __init__(self, model="mistral"):
        self.model = model

    def generate(self, prompt: str) -> str:
        print("slflj")
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
