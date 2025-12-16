from pathlib import Path
from app.ai.ollama_llm import OllamaLLM


class ReleaseRiskAIEngine:
    def __init__(self, llm):
        self.llm = llm
        self.prompt_template = (
            Path(__file__).parent / "prompt_template.txt"
        ).read_text(encoding="utf-8")

    def generate(self, payload):
        prompt = self.prompt_template.format(
            risk_score=payload["risk_score"],
            risk_level=payload["risk_level"],
            test_failure_rate=payload["metrics"]["test_failure_rate"],
            test_trend=payload["metrics"]["test_trend"],
            commit_churn=payload["metrics"]["commit_churn"],
            critical_defects=payload["metrics"]["defects"]["critical"],
            high_defects=payload["metrics"]["defects"]["high"],
            pipeline_stability=payload["metrics"]["pipeline_stability"]
        )
        return self.llm.generate(prompt)

