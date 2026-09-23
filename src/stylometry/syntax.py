def pos_features(text: str) -> dict:
    try:
        import nltk
    except ImportError:
        return {'status': 'nltk_not_available'}
        
    try:
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        # fallback for older nltk versions
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
        tokens = nltk.word_tokenize(text)
        if not tokens:
            return {
                "status": "success", 
                "pos_distribution": {}, 
                "noun_ratio": 0.0, 
                "verb_ratio": 0.0, 
                "adjective_ratio": 0.0, 
                "adverb_ratio": 0.0, 
                "function_to_content_ratio": 0.0
            }
            
        tags = nltk.pos_tag(tokens)
        
        pos_dist = {}
        nouns = verbs = adjs = advs = 0
        total = len(tags)
        
        for word, tag in tags:
            pos_dist[tag] = pos_dist.get(tag, 0) + 1
            if tag.startswith('NN'):
                nouns += 1
            elif tag.startswith('VB'):
                verbs += 1
            elif tag.startswith('JJ'):
                adjs += 1
            elif tag.startswith('RB'):
                advs += 1
                
        pos_distribution = {tag: count / total for tag, count in pos_dist.items()}
        
        content_words = nouns + verbs + adjs + advs
        function_words = total - content_words
        function_to_content_ratio = function_words / content_words if content_words > 0 else float('inf')
        
        return {
            "status": "success",
            "pos_distribution": pos_distribution,
            "noun_ratio": nouns / total,
            "verb_ratio": verbs / total,
            "adjective_ratio": adjs / total,
            "adverb_ratio": advs / total,
            "function_to_content_ratio": function_to_content_ratio
        }
    except Exception as e:
        # If any NLTK processing fails, return a safe fallback or error dict
        return {'status': 'nltk_error', 'message': str(e)}
