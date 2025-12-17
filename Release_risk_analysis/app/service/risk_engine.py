from app.ingestion.csv_loader import load_csv
from app.ingestion.validator import validate, extract_single_release_id

from app.metrics import (
    test_metrics,
    commit_metrics,
    defect_metrics,
    pipeline_metrics
)

from app.risk.scorer import score
from app.risk.mapper import map_level
from app.config import CSV_PATHS


def run_engine():
    # ---- Load raw CSVs
    tests_df = load_csv(CSV_PATHS["tests"])
    commits_df = load_csv(CSV_PATHS["commits"])
    defects_df = load_csv(CSV_PATHS["defects"])
    pipelines_df = load_csv(CSV_PATHS["pipelines"])

    # ---- Extract release_id from each file
    release_ids = {
        extract_single_release_id(tests_df),
        extract_single_release_id(commits_df),
        extract_single_release_id(defects_df),
        extract_single_release_id(pipelines_df),
    }

    if len(release_ids) != 1:
        raise ValueError(
            f"Release ID mismatch across files: {list(release_ids)}"
        )

    release_id = release_ids.pop()

    # ---- Validate schemas & filter by release_id
    tests = validate(
        tests_df,
        {"test_date", "total_tests", "failed_tests", "release_id"},
        release_id
    )

    commits = validate(
        commits_df,
        {"commit_date", "commit_count", "release_id"},
        release_id
    )

    defects = validate(
        defects_df,
        {"severity", "status", "release_id"},
        release_id
    )

    pipelines = validate(
        pipelines_df,
        {"pipeline_status", "release_id"},
        release_id
    )

    # ---- Metrics
    test_rate, test_trend = test_metrics.calculate(tests)
    churn = commit_metrics.calculate(commits)
    defect_counts = defect_metrics.calculate(defects)
    pipeline = pipeline_metrics.calculate(pipelines)

    risk = score(
        test_rate,
        churn,
        defect_counts["critical"],
        pipeline
    )

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
