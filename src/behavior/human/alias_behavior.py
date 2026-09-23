import re
from typing import List, Dict, Any
from .models import HumanBehaviorSignal

def analyze_aliases(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze posts to extract and analyze alias behavior such as reuse and mutation.
    Returns a list of HumanBehaviorSignal dictionaries.
    """
    signals = []
    
    # Extract unique authors
    authors = set()
    author_posts = {}
    for post in posts:
        author = post.get('author_id') or post.get('author') or post.get('username')
        if author:
            author_str = str(author).strip()
            authors.add(author_str)
            if author_str not in author_posts:
                author_posts[author_str] = []
            post_id = post.get('id') or post.get('post_id')
            if post_id:
                author_posts[author_str].append(str(post_id))

    # Look for alias mutations (e.g. user, user99, user_123)
    # This is a basic observation check
    authors_list = list(authors)
    mutations_found = set()
    
    for i, author1 in enumerate(authors_list):
        for j in range(i + 1, len(authors_list)):
            author2 = authors_list[j]
            # Simple heuristic: one is a prefix of the other, or they share a large common prefix
            # and differ by numbers/special characters.
            base1 = re.sub(r'[^a-zA-Z]', '', author1).lower()
            base2 = re.sub(r'[^a-zA-Z]', '', author2).lower()
            
            if base1 and base1 == base2 and author1 != author2:
                # We found a mutation
                mutation_pair = frozenset([author1, author2])
                if mutation_pair not in mutations_found:
                    mutations_found.add(mutation_pair)
                    
                    evidence_ids = author_posts.get(author1, []) + author_posts.get(author2, [])
                    
                    signal = HumanBehaviorSignal(
                        category='identity',
                        signal_type='ALIAS_MUTATION',
                        observations=[f"Observed similar handles: '{author1}' and '{author2}'"],
                        evidence_ids=list(set(evidence_ids)),
                        confidence=0.6,
                        explanation="Similarity in alphabetic characters of aliases suggests potential mutation or reuse of naming conventions.",
                        limitations=["Different actors may use similar base names coincidentally.", "Does not confirm same identity."]
                    )
                    signals.append(signal.model_dump())
                    
    # Look for alias reuse across multiple posts
    for author, p_ids in author_posts.items():
        if len(p_ids) > 1:
            signal = HumanBehaviorSignal(
                category='identity',
                signal_type='ALIAS_REUSE',
                observations=[f"Handle '{author}' reused across {len(p_ids)} observations."],
                evidence_ids=list(set(p_ids)),
                confidence=0.9,
                explanation="Repeated use of the exact handle in the provided dataset.",
                limitations=["Handle could be a default or generic term.", "Account sharing is possible."]
            )
            signals.append(signal.model_dump())

    return signals
