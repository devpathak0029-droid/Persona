from collections import Counter
import re

PUNCT = ".,!?;:'\"-()[]{}—"

def punctuation_features(text: str) -> dict:
    counts = Counter(c for c in text if c in PUNCT)
    n = max(len(text), 1)
    
    features = {c: counts[c] / n for c in PUNCT}
    
    features['single_quotes'] = counts.get("'", 0) / n
    features['double_quotes'] = counts.get('"', 0) / n
    
    bracket_chars = "()[]{}"
    features['brackets'] = sum(counts.get(c, 0) for c in bracket_chars) / n
    
    hyphen_chars = "-—"
    features['hyphens'] = sum(counts.get(c, 0) for c in hyphen_chars) / n
    
    # Repeated punctuation
    repeated = {
        '!!': len(re.findall(r'!!', text)),
        '??': len(re.findall(r'\?\?', text)),
        '...': len(re.findall(r'\.\.\.', text)),
        '!!!': len(re.findall(r'!!!', text)),
        '???': len(re.findall(r'\?\?\?', text))
    }
    features['repeated_punctuation'] = repeated
    
    # Spacing after period
    total_periods = text.count('.')
    space_after_periods = text.count('. ')
    features['spacing_after_period'] = space_after_periods / total_periods if total_periods > 0 else 0.0
    
    return features
