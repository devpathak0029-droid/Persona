def emoji_features(text: str) -> dict:
    chars = [c for c in text if ord(c) > 0x1F300]
    return {
        "emoji_count": len(chars),
        "emoji_vocabulary": sorted(set(chars))
    }
