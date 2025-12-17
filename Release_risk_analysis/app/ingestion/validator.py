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

def extract_single_release_id(df):
    if "release_id" not in df.columns:
        raise ValueError("Missing 'release_id' column")

    release_ids = df["release_id"].dropna().unique()

    if len(release_ids) != 1:
        raise ValueError(
            f"Expected exactly one release_id, found: {list(release_ids)}"
        )

    return release_ids[0]
