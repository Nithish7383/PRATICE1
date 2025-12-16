def calculate(df):
    df["status"] = df["status"].astype(str).str.upper().str.strip()
    df["severity"] = df["severity"].astype(str).str.lower().str.strip()

    open_df = df[df.status == "OPEN"]

    return {
        "critical": int((open_df.severity == "critical").sum()),
        "high": int((open_df.severity == "high").sum()),
        "medium": int((open_df.severity == "medium").sum()),
    }
