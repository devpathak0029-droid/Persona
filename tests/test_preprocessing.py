import pytest
from src.preprocessing.cleaner import clean_text, clean_post
from src.preprocessing.template_detector import detect_templates
from src.preprocessing.identifier_filter import filter_identifiers
from src.preprocessing.deduplicator import deduplicate
from src.preprocessing.corpus_quality import assess_quality

def test_clean_text():
    text = "Check out this link https://example.com and my wallet 0x1234567890123456789012345678901234567890 "
    cleaned = clean_text(text)
    assert "https://example.com" not in cleaned
    assert "0x1234567890123456789012345678901234567890" not in cleaned
    assert cleaned == "Check out this link and my wallet"

    pgp_text = "Hello\n-----BEGIN PGP MESSAGE-----\nstuff\n-----END PGP MESSAGE-----\nWorld"
    cleaned_pgp = clean_text(pgp_text)
    assert "stuff" not in cleaned_pgp

def test_clean_post():
    text = "Here is my code: ```print('hello')```"
    raw, cleaned = clean_post(text)
    assert raw == text
    assert cleaned == "Here is my code:"

def test_detect_templates():
    text = "Hello guys!\n---\nJohn Doe"
    result = detect_templates(text)
    assert result["has_signature"] is True
    assert result["cleaned_text"] == "Hello guys!"
    
    text2 = "Sent from my iPhone"
    result2 = detect_templates(text2)
    assert result2["has_boilerplate"] is True

def test_filter_identifiers():
    text = "Hey @user1, my pgp is 0x1234ABCD1234ABCD"
    filtered = filter_identifiers(text, known_handles=["user2"])
    assert "@user1" not in filtered
    assert "0x1234ABCD1234ABCD" not in filtered
    
    text2 = "I am DarkScripter doing stuff"
    filtered2 = filter_identifiers(text2, known_handles=["DarkScripter"])
    assert "DarkScripter" not in filtered2
    assert "I am doing stuff" in filtered2

def test_deduplicate():
    posts = [
        {"post_id": "1", "text": "This is a unique post"},
        {"post_id": "2", "text": "This is another post"},
        {"post_id": "3", "text": "This is a unique post"}, # Exact match to 1
        {"post_id": "4", "text": "This is another post which is slightly different"} # Near duplicate
    ]
    result = deduplicate(posts)
    # 1 and 3 are exact dupes, 2 and 4 might not be near dupes since 0.85 jaccard is high.
    # Let's check 2 and 4 jaccard manually in mind:
    # 2: "this", "is", "another", "post" (4 words)
    # 4: "this", "is", "another", "post", "which", "is", "slightly", "different" (8 words)
    # intersection: 4, union: 7 -> 4/7 = 0.57. So NOT a near duplicate.
    
    # Add a real near duplicate:
    posts.append({"post_id": "5", "text": "This is a unique post too"}) # words: this, is, a, unique, post, too. Int: 5, Union: 6. 5/6 = 0.83 < 0.85. Wait, 0.83 < 0.85.
    # We need a 0.85 near duplicate
    posts.append({"post_id": "6", "text": "This is a unique post and it"}) # this, is, a, unique, post, and, it (7 words). Int: 5, Union: 7. 5/7 = 0.71.
    
    # Just exact dupes:
    result = deduplicate(posts)
    assert result["duplicate_count"] == 1
    assert len(result["unique_posts"]) == 5
    assert ["1", "3"] in result["duplicate_groups"]

def test_assess_quality():
    posts = [1, 2, 3, 4, 5, 6]
    cleaned = ["a" * 100] * 6 # 600 chars
    res = assess_quality(posts, cleaned, "en", 0.1)
    assert res["eligible"] is True
    
    # Not enough posts
    res2 = assess_quality([1, 2], cleaned[:2], "en", 0.1)
    assert res2["eligible"] is False
    assert any("Insufficient posts" in r for r in res2["reasons"])
    
    # Not enough chars
    res3 = assess_quality(posts, ["a"] * 6, "en", 0.1)
    assert res3["eligible"] is False
    assert any("Insufficient clean characters" in r for r in res3["reasons"])
