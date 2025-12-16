from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CSV_PATHS = {
    "tests": DATA_DIR / "test_results.csv",
    "commits": DATA_DIR / "commit_activity.csv",
    "defects": DATA_DIR / "defects.csv",
    "pipelines": DATA_DIR / "pipeline_runs.csv",
}
