def calculate(df):
    df["pipeline_status"] = df["pipeline_status"].astype(str).str.upper().str.strip()

    failed = (df.pipeline_status == "FAILED").sum()
    total = len(df)

    ratio = failed / total if total else 0

    if ratio <= 0.10:
        return "Stable"
    elif ratio <= 0.30:
        return "Degraded"
    else:
        return "Unstable"
