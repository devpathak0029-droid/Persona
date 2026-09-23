try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def extract_topics(texts: list[str], n_topics: int = 5, top_words_per_topic: int = 8) -> dict:
    """
    Extracts topics from a list of texts using TF-IDF and KMeans clustering.
    """
    if not SKLEARN_AVAILABLE:
        return {
            'topics': [],
            'document_topic_assignments': [],
            'n_topics_found': 0,
            'method': 'tfidf_kmeans',
            'explanation': 'scikit-learn is not installed.'
        }
        
    if len(texts) < 3:
        return {
            'topics': [],
            'document_topic_assignments': [],
            'n_topics_found': 0,
            'method': 'tfidf_kmeans',
            'explanation': 'Too few texts for topic extraction (minimum 3 required).'
        }
        
    # Remove empty texts
    texts = [t for t in texts if t.strip()]
    if len(texts) < 3:
        return {
            'topics': [],
            'document_topic_assignments': [],
            'n_topics_found': 0,
            'method': 'tfidf_kmeans',
            'explanation': 'Too few non-empty texts for topic extraction.'
        }

    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        # Happens if vocab is empty after stop words/min_df
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
        except ValueError:
            return {
                'topics': [],
                'document_topic_assignments': [],
                'n_topics_found': 0,
                'method': 'tfidf_kmeans',
                'explanation': 'Vocabulary is empty after removing stop words.'
            }

    num_clusters = min(n_topics, len(texts))
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(tfidf_matrix)

    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    topics = []
    for i in range(num_clusters):
        top_words = [terms[ind] for ind in order_centroids[i, :top_words_per_topic]]
        # Calculate topic weight by number of documents assigned
        weight = float(sum(kmeans.labels_ == i)) / len(texts)
        topics.append({
            'topic_id': i,
            'top_words': top_words,
            'weight': weight
        })

    return {
        'topics': topics,
        'document_topic_assignments': kmeans.labels_.tolist(),
        'n_topics_found': num_clusters,
        'method': 'tfidf_kmeans'
    }

def topic_overlap(topics_a: dict, topics_b: dict) -> dict:
    """
    Compares two topic extractions and computes Jaccard similarity.
    """
    if not topics_a.get('topics') or not topics_b.get('topics'):
        return {
            'topic_similarity': 0.0,
            'shared_terms': [],
            'unique_to_a': [],
            'unique_to_b': [],
            'explanation': 'One or both topic dictionaries are empty.'
        }

    words_a = set()
    for t in topics_a['topics']:
        words_a.update(t['top_words'])
        
    words_b = set()
    for t in topics_b['topics']:
        words_b.update(t['top_words'])
        
    shared = words_a.intersection(words_b)
    union = words_a.union(words_b)
    
    similarity = float(len(shared) / len(union)) if union else 0.0
    
    unique_a = words_a - words_b
    unique_b = words_b - words_a
    
    return {
        'topic_similarity': similarity,
        'shared_terms': list(shared),
        'unique_to_a': list(unique_a),
        'unique_to_b': list(unique_b),
        'explanation': f"Found {len(shared)} shared terms, Jaccard similarity is {similarity:.4f}."
    }
