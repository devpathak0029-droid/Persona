import sys
import os
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import json

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.post import Post
from src.persona.profile_builder import build_profile


def parse_raaj7z_blog(html_path: str):
    print(f"[*] Reading target blog: {html_path}")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Extract Author & Identity Info
    author_elem = soup.find("h1", class_="author-name")
    author_name = author_elem.text.strip() if author_elem else "raaj.7z"

    # 2. Extract Crypto Wallets
    wallets = {}
    for code in soup.find_all("code", class_="crypto-addr"):
        coin = code.get("data-coin", "UNKNOWN")
        wallets[coin] = code.text.strip()

    # 3. Extract PGP Block
    pgp_elem = soup.find("pre", class_="pgp-box")
    pgp_key = pgp_elem.text.strip() if pgp_elem else None

    # 4. Extract Articles / Posts for Stylometry & Behavioral Analysis
    posts = []
    articles = soup.find_all("article", class_="post-card")
    for idx, art in enumerate(articles):
        post_id = art.get("data-post-id", f"post_{idx}")
        author = art.get("data-author", author_name)
        ts_str = art.get("data-timestamp")
        
        timestamp = None
        if ts_str:
            try:
                timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except Exception:
                timestamp = datetime.utcnow()

        body_elem = art.find("div", class_="post-body")
        text = body_elem.get_text(separator="\n").strip() if body_elem else ""

        posts.append(Post(
            post_id=post_id,
            author_id=author,
            platform="darkweb_blog",
            text=text,
            timestamp=timestamp,
            raw_text=text,
            metadata={"wallets": wallets, "has_pgp": pgp_key is not None}
        ))

    print(f"[+] Successfully extracted {len(posts)} posts from target {author_name}")
    print(f"[+] Extracted Crypto Tokens: {list(wallets.keys())}")
    for coin, addr in wallets.items():
        print(f"    - {coin}: {addr}")

    # 5. Execute Full Persona Analysis
    print("\n[*] Running PRALAYX Persona Profiler on target...")
    profile = build_profile(persona_id=author_name, posts=posts)

    print("\n================ PERSONA ANALYSIS RESULTS ================")
    print(f"Persona ID: {profile.get('persona_id')}")
    print(f"Corpus Eligible: {profile.get('corpus_quality', {}).get('eligible')}")
    print(f"Post Count: {profile.get('corpus_quality', {}).get('post_count')}")
    print(f"Character Count: {profile.get('corpus_quality', {}).get('character_count')}")
    
    # Stylometry summary
    stylo = profile.get("stylometry", {})
    if stylo:
        print("\n--- Stylometric Signals ---")
        print(f"Avg Word Length: {stylo.get('lexical', {}).get('avg_word_length', 0):.2f}")
        print(f"Type-Token Ratio: {stylo.get('lexical', {}).get('type_token_ratio', 0):.2f}")
        print(f"Mean Sentence Length: {stylo.get('sentence_structure', {}).get('mean_sentence_length', 0):.2f}")
        print(f"Function Words Total Categories: {len(stylo.get('function_words', {}).get('category_totals', {}))}")

    # Human behavior signals
    human_beh = profile.get("human_behavior", {})
    if human_beh:
        print("\n--- Human-Behavior Signals ---")
        for sig in human_beh.get("signals", []):
            print(f"[{sig.get('signal_type')}] ({sig.get('confidence')*100:.0f}% conf): {sig.get('explanation')}")

    # Save complete output
    output_path = "raaj7z_persona_profile.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(profile, out, indent=2, default=str)
    print(f"\n[+] Full profile output saved to: {output_path}")


if __name__ == "__main__":
    parse_raaj7z_blog("../test_target_raaj7z.html")
