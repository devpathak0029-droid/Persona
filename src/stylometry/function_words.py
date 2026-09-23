FUNCTION_WORDS = {
    'articles': ['the', 'a', 'an'],
    'pronouns': ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'ours', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves', 'this', 'that', 'these', 'those', 'who', 'whom', 'which', 'what'],
    'prepositions': ['in', 'on', 'at', 'to', 'for', 'with', 'from', 'by', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'against', 'without', 'within'],
    'auxiliaries': ['is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did'],
    'conjunctions': ['and', 'or', 'but', 'nor', 'yet', 'so', 'because', 'although', 'while', 'if', 'then', 'unless', 'until', 'whether'],
    'modals': ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'need', 'dare']
}

def function_word_features(text: str) -> dict:
    words = text.lower().split()
    total = max(len(words), 1)
    
    flat_words = [word for category in FUNCTION_WORDS.values() for word in category]
    
    # per-word frequencies
    features = {w: words.count(w) / total for w in sorted(flat_words)}
    
    # category totals
    category_totals = {}
    for cat, cat_words in FUNCTION_WORDS.items():
        category_totals[cat] = sum(words.count(w) for w in cat_words) / total
    features['category_totals'] = category_totals
    
    # person ratios
    first_person_words = {'i', 'me', 'my', 'mine', 'myself'}
    third_person_words = {'he', 'she', 'it', 'they', 'him', 'her', 'them', 'his', 'its', 'their', 'theirs', 'himself', 'herself', 'itself', 'themselves'}
    
    features['first_person_ratio'] = sum(words.count(w) for w in first_person_words) / total
    features['third_person_ratio'] = sum(words.count(w) for w in third_person_words) / total
    
    return features
