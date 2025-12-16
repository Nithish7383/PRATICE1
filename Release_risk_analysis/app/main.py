from app.service.risk_engine import run_engine
from app.ai.ollama_llm import OllamaLLM
from app.ai.release_risk_ai import ReleaseRiskAIEngine

if __name__ == "__main__":
    result = run_engine("BILLING_SERVICE_REL_2025_Q4")

    llm = OllamaLLM(model="mistral")
    ai = ReleaseRiskAIEngine(llm)

    ai_output = ai.generate(result)

    print("===== FINAL OUTPUT =====")
    print(ai_output)
