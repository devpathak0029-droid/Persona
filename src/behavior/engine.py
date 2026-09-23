from .temporal import temporal_features
from .frequency import frequency_features
from .burst import detect_bursts, detect_inactivity
from .lifecycle import analyze_lifecycle
from .platform import platform_activity

def analyze_behavior(posts: list) -> dict:
    return {
        "temporal": temporal_features(posts),
        "frequency": frequency_features(posts),
        "bursts": detect_bursts(posts),
        "inactive_periods": detect_inactivity(posts),
        "lifecycle": analyze_lifecycle(posts),
        "platform_activity": platform_activity(posts)
    }
