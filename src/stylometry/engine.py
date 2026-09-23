from .lexical import lexical_features
from .function_words import function_word_features
from .punctuation import punctuation_features
from .sentence_structure import sentence_features
from .ngrams import character_ngrams
from .spelling import spelling_features
from .emoji import emoji_features

def analyze_style(text: str) -> dict:
    return {
        "lexical": lexical_features(text),
        "function_words": function_word_features(text),
        "punctuation": punctuation_features(text),
        "sentence_structure": sentence_features(text),
        "character_ngrams": character_ngrams(text, 3),
        "spelling": spelling_features(text),
        "emoji": emoji_features(text)
    }
