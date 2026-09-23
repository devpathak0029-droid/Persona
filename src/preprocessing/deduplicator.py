import hashlib

def _jaccard_similarity(set1: set[str], set2: set[str]) -> float:
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 1.0 if not set1 and not set2 else 0.0
    return len(intersection) / len(union)

def deduplicate(posts: list[dict]) -> dict:
    """
    Detects duplicate and near-duplicate posts using exact hashing and Jaccard similarity.
    Each post dict must have 'post_id' and 'text'.
    """
    unique_posts = []
    duplicate_groups = []
    seen_hashes = {}
    
    # Track word sets for near-duplicate comparison
    unique_word_sets = []

    duplicate_count = 0

    for post in posts:
        text = post.get("text", "")
        post_id = post.get("post_id")
        
        # Exact match
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        is_duplicate = False
        if text_hash in seen_hashes:
            is_duplicate = True
            # Find the group
            original_id = seen_hashes[text_hash]
            added_to_group = False
            for group in duplicate_groups:
                if original_id in group:
                    group.append(post_id)
                    added_to_group = True
                    break
            if not added_to_group:
                duplicate_groups.append([original_id, post_id])
        else:
            # Check near-duplicate
            words = set(text.lower().split())
            for idx, (orig_id, orig_words) in enumerate(unique_word_sets):
                if _jaccard_similarity(words, orig_words) >= 0.85:
                    is_duplicate = True
                    # Add to group
                    added_to_group = False
                    for group in duplicate_groups:
                        if orig_id in group:
                            group.append(post_id)
                            added_to_group = True
                            break
                    if not added_to_group:
                        duplicate_groups.append([orig_id, post_id])
                    break
            
            if not is_duplicate:
                seen_hashes[text_hash] = post_id
                unique_word_sets.append((post_id, words))
                unique_posts.append(post)

        if is_duplicate:
            duplicate_count += 1

    total_posts = len(posts)
    duplicate_ratio = duplicate_count / total_posts if total_posts > 0 else 0.0

    return {
        "unique_posts": unique_posts,
        "duplicate_count": duplicate_count,
        "duplicate_ratio": duplicate_ratio,
        "duplicate_groups": duplicate_groups
    }
