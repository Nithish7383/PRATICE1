def calculate(df):
    avg = df.commit_count.mean()

    if avg < 10:
        return "Low"
    elif avg <= 25:
        return "Medium"
    else:
        return "High"
