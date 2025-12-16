def map_level(score):
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    else:
        return "High"
