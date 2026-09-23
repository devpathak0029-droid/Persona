import re

def emoji_features(text: str) -> dict:
    chars = [c for c in text if ord(c) > 0x1F300]
    emoji_count = len(chars)
    emoji_ratio = emoji_count / max(len(text), 1)
    
    emoticon_pattern = r"(?::|;|=)(?:-)?(?:\)|\(|D|P)|(?:X|x)D|<3"
    emoticons = re.findall(emoticon_pattern, text)
    
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    position_dist = {'start': 0, 'middle': 0, 'end': 0}
    
    for s in sentences:
        for i, c in enumerate(s):
            if ord(c) > 0x1F300:
                ratio = i / len(s)
                if ratio < 0.2:
                    position_dist['start'] += 1
                elif ratio > 0.8:
                    position_dist['end'] += 1
                else:
                    position_dist['middle'] += 1
                    
    return {
        "emoji_count": emoji_count,
        "emoji_vocabulary": sorted(set(chars)),
        "emoji_ratio": emoji_ratio,
        "emoticons": emoticons,
        "emoticon_count": len(emoticons),
        "position_distribution": position_dist
    }
