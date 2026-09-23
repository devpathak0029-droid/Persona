from .temporal import temporal_features
from .frequency import frequency_features

def analyze_behavior(posts: list) -> dict:
    return {
        "temporal": temporal_features(posts),
        "frequency": frequency_features(posts)
    }
