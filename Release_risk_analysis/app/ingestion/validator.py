def validate(df, required_cols, release_id):
    # column check
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # release_id normalization
    df["release_id"] = df["release_id"].astype(str).str.strip()
    if df["release_id"].nunique() != 1 or df["release_id"].iloc[0] != release_id:
        raise ValueError("release_id mismatch")

    # null handling
    df = df.fillna(0)

    return df
