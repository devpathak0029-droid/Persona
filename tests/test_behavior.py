import pytest
from datetime import datetime, timedelta
from typing import Optional

from src.behavior.temporal import temporal_features
from src.behavior.frequency import frequency_features
from src.behavior.burst import detect_bursts, detect_inactivity
from src.behavior.lifecycle import analyze_lifecycle
from src.behavior.platform import platform_activity

class MockPost:
    def __init__(self, timestamp: Optional[datetime] = None, platform: str = None):
        self.timestamp = timestamp
        self.platform = platform

def test_temporal_features():
    posts = [
        MockPost(timestamp=datetime(2023, 1, 1, 12, 0, 0)), # Sunday
        MockPost(timestamp=datetime(2023, 1, 2, 13, 0, 0)), # Monday
        MockPost(timestamp=datetime(2023, 1, 2, 14, 0, 0)),
        MockPost(timestamp=datetime(2023, 1, 3, 12, 0, 0)),
    ]
    res = temporal_features(posts)
    assert res["weekend_ratio"] == 0.25 # 1 out of 4 is Sunday
    assert res["activity_window"]["peak_hour"] == 12 # 12 appears twice
    assert 0 <= res["timezone_consistency"] <= 1.0

def test_frequency_features():
    posts = [
        MockPost(timestamp=datetime(2023, 1, 1, 10, 0, 0)),
        MockPost(timestamp=datetime(2023, 1, 1, 12, 0, 0)), # gap 2
        MockPost(timestamp=datetime(2023, 1, 1, 15, 0, 0)), # gap 3
    ]
    res = frequency_features(posts)
    assert res["timestamped_posts"] == 3
    assert res["min_gap_hours"] == 2.0
    assert res["max_gap_hours"] == 3.0
    assert res["avg_gap_hours"] == 2.5
    assert res["total_active_days"] == 1

def test_bursts():
    posts = [
        MockPost(timestamp=datetime(2023, 1, 1, 10, 0, 0)),
        MockPost(timestamp=datetime(2023, 1, 1, 10, 30, 0)),
        MockPost(timestamp=datetime(2023, 1, 1, 10, 45, 0)), # burst 1
        MockPost(timestamp=datetime(2023, 1, 5, 10, 0, 0)),  # far away
        MockPost(timestamp=datetime(2023, 1, 6, 10, 0, 0))   # far away
    ]
    res = detect_bursts(posts, gap_threshold_hours=1.0)
    assert res["burst_count"] == 1
    assert res["posts_in_bursts"] == 3
    assert res["burst_ratio"] == 0.6
    
    inact = detect_inactivity(posts, threshold_days=2)
    assert len(inact) == 1
    assert inact[0]["duration_days"] > 3.0

def test_lifecycle():
    posts = [
        MockPost(timestamp=datetime(2023, 1, 1)),
        MockPost(timestamp=datetime(2023, 1, 2)),
        MockPost(timestamp=datetime(2023, 1, 3)), # early
        MockPost(timestamp=datetime(2023, 2, 1)),
        MockPost(timestamp=datetime(2023, 2, 2)), 
        MockPost(timestamp=datetime(2023, 2, 3)), # middle
        MockPost(timestamp=datetime(2023, 3, 1)),
        MockPost(timestamp=datetime(2023, 3, 2)),
        MockPost(timestamp=datetime(2023, 3, 3)), # late
    ]
    res = analyze_lifecycle(posts)
    assert res["stage"] in ["emerging", "declining", "active", "dormant"]
    assert "early" in res["periods"]
    assert "late" in res["periods"]

def test_platform():
    posts = [
        MockPost(timestamp=datetime(2023, 1, 1), platform="twitter"),
        MockPost(timestamp=datetime(2023, 1, 2), platform="twitter"),
        MockPost(timestamp=datetime(2023, 1, 3), platform="reddit"),
    ]
    res = platform_activity(posts)
    assert res["platform_count"] == 2
    assert res["primary_platform"] == "twitter"
    assert res["cross_platform"] is True
    assert res["platforms"]["twitter"] == 2
    assert res["platforms"]["reddit"] == 1
    assert "reddit" in res["platform_timeline"]
