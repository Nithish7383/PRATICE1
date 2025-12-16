def calculate(df):
    total = df.total_tests.sum()
    failed = df.failed_tests.sum()

    if total == 0:
        rate = 0.0
    else:
        rate = (failed / total) * 100

    rate = float(round(rate, 2))

    # simple trend (safe default)
    trend = "Stable"

    return rate, trend
