from pydantic import BaseModel
from typing import Literal

class Defects(BaseModel):
    critical: int
    high: int
    medium: int

class Metrics(BaseModel):
    test_failure_rate: float
    test_trend: Literal["Improving","Stable","Worsening"]
    commit_churn: Literal["Low","Medium","High"]
    defects: Defects
    pipeline_stability: Literal["Stable","Degraded","Unstable"]

class Output(BaseModel):
    release_id: str
    risk_score: int
    risk_level: Literal["Low","Medium","High"]
    metrics: Metrics