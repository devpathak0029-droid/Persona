from collections import Counter

def lexical_features(text: str) -> dict:
    words = [w.lower() for w in text.split() if w.strip()]
    n = len(words)
    if not n:
        return {"word_count": 0}
    counts = Counter(words)
    
    vocab_freq_counts = {"1x": 0, "2x": 0, "3x": 0, "4x": 0, "5+x": 0}
    for count in counts.values():
        if count == 1: vocab_freq_counts["1x"] += 1
        elif count == 2: vocab_freq_counts["2x"] += 1
        elif count == 3: vocab_freq_counts["3x"] += 1
        elif count == 4: vocab_freq_counts["4x"] += 1
        else: vocab_freq_counts["5+x"] += 1
        
    unique_n = len(counts)
    vocab_freq = {k: v / unique_n for k, v in vocab_freq_counts.items()} if unique_n else {}
    rare_word_ratio = (vocab_freq_counts["1x"] + vocab_freq_counts["2x"]) / unique_n if unique_n else 0.0
    
    phrases = []
    for i in range(len(words) - 1):
        phrases.append(f"{words[i]} {words[i+1]}")
    for i in range(len(words) - 2):
        phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    repeated_phrases = Counter(phrases).most_common(15)

    return {
        "word_count": n,
        "unique_words": unique_n,
        "type_token_ratio": unique_n / n,
        "hapax_ratio": sum(v == 1 for v in counts.values()) / n,
        "avg_word_length": sum(map(len, words)) / n,
        "top_words": counts.most_common(20),
        "vocabulary_frequency": vocab_freq,
        "rare_word_ratio": rare_word_ratio,
        "repeated_phrases": repeated_phrases
    }
