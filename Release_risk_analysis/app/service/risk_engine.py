from ingestion.csv_loader import load_csv
from ingestion.validator import validate
from metrics import test_metrics, commit_metrics, defect_metrics, pipeline_metrics
from risk.scorer import score
from risk.mapper import map_level
from config import CSV_PATHS
from app.ingestion.validator import validate


def run_engine(release_id):
    tests = validate(
        load_csv(CSV_PATHS["tests"]),
        {"test_date", "total_tests", "failed_tests", "release_id"},
        release_id
    )

    commits = validate(
        load_csv(CSV_PATHS["commits"]),
        {"commit_date", "commit_count", "release_id"},
        release_id
    )

    defects = validate(
        load_csv(CSV_PATHS["defects"]),
        {"severity", "status", "release_id"},
        release_id
    )

    pipelines = validate(
        load_csv(CSV_PATHS["pipelines"]),
        {"pipeline_status", "release_id"},
        release_id
    )

    test_rate, test_trend = test_metrics.calculate(tests)
    churn = commit_metrics.calculate(commits)
    defect_counts = defect_metrics.calculate(defects)
    pipeline = pipeline_metrics.calculate(pipelines)

    # # 🔎 DEBUG (remove later)
    # print("DEBUG → test_rate:", test_rate)
    # print("DEBUG → churn:", churn)
    # print("DEBUG → critical defects:", defect_counts["critical"])
    # print("DEBUG → pipeline:", pipeline)

    risk = score(test_rate, churn, defect_counts["critical"], pipeline)

    return {
        "release_id": release_id,
        "risk_score": risk,
        "risk_level": map_level(risk),
        "metrics": {
            "test_failure_rate": test_rate,
            "test_trend": test_trend,
            "commit_churn": churn,
            "defects": defect_counts,
            "pipeline_stability": pipeline
        }
    }
