FUNCTION_WORDS = {
    "the","a","an","and","or","but","if","then","of","to","in","on","for",
    "with","from","by","as","is","are","was","were","be","been","it","this",
    "that","i","you","he","she","we","they","my","your","our","their"
}

def function_word_features(text: str) -> dict:
    words = text.lower().split()
    total = max(len(words), 1)
    return {w: words.count(w) / total for w in sorted(FUNCTION_WORDS)}
