def score(test_rate, churn, critical, pipeline):
    score = 0
    score += test_rate * 0.35
    score += {"Low": 10, "Medium": 20, "High": 30}[churn] * 0.2
    score += min(critical * 5, 25)
    score += {"Stable": 5, "Degraded": 15, "Unstable": 25}[pipeline]
    return int(min(score, 100))
