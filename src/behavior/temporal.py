from collections import Counter

def temporal_features(posts: list) -> dict:
    hours = Counter()
    weekdays = Counter()
    for p in posts:
        if p.timestamp:
            hours[p.timestamp.hour] += 1
            weekdays[p.timestamp.weekday()] += 1
    return {
        "posting_hours": dict(hours),
        "weekday_distribution": dict(weekdays)
    }
