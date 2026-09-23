import pytest
from src.stylometry.lexical import lexical_features
from src.stylometry.function_words import function_word_features
from src.stylometry.punctuation import punctuation_features
from src.stylometry.sentence_structure import sentence_features
from src.stylometry.ngrams import multi_ngrams, character_ngrams
from src.stylometry.spelling import spelling_features
from src.stylometry.emoji import emoji_features
from src.stylometry.syntax import pos_features

def test_lexical_features():
    text = "hello world hello"
    res = lexical_features(text)
    assert res["word_count"] == 3
    assert res["unique_words"] == 2
    assert res["type_token_ratio"] == 2/3
    assert res["hapax_ratio"] == 1/3
    assert res["rare_word_ratio"] == 1.0 # 2 unique, both frequency < 3 => 1x and 2x. hello is 2x, world is 1x. Both sum to 2. 2/2 = 1.0

def test_function_words():
    text = "the dog and the cat run to me"
    res = function_word_features(text)
    assert 'category_totals' in res
    assert res['category_totals']['articles'] == 2/8  # 'the', 'the'
    assert res['first_person_ratio'] == 1/8  # 'me'
    assert res['third_person_ratio'] == 0/8

def test_punctuation_features():
    text = "hello!! wait, what?? no..."
    res = punctuation_features(text)
    assert res['!'] == 2/len(text)
    assert res['?'] == 2/len(text)
    assert res['.'] == 3/len(text)
    assert res['repeated_punctuation']['!!'] == 1
    assert res['repeated_punctuation']['??'] == 1
    assert res['repeated_punctuation']['...'] == 1

def test_sentence_features():
    text = "Do this! What is that? I think so."
    res = sentence_features(text)
    assert res["sentence_count"] == 3
    assert res["question_ratio"] == 1/3
    assert res["exclamation_ratio"] == 1/3
    assert res["imperative_indicators"] == 1 # "do"

def test_ngrams():
    text = "hello"
    res = multi_ngrams(text)
    assert "3gram" in res
    assert "4gram" in res
    assert "5gram" in res
    assert "hel" in res["3gram"]
    assert "ell" in res["3gram"]
    assert "llo" in res["3gram"]

def test_spelling():
    text = "HELLO im UR frenddd and you're coOl!"
    res = spelling_features(text)
    assert res["all_caps_token_ratio"] > 0
    assert "frenddd" in dict(res["repeated_character_tokens"])
    assert res["abbreviation_count"] == 1 # "ur"
    assert res["apostrophe_usage"]["im"] == 1
    assert res["apostrophe_usage"]["you're"] == 1
    assert res["mixed_case_tokens"] == 1 # "coOl"

def test_emoji():
    text = "hello 😊! This is great 🚀xD"
    res = emoji_features(text)
    assert res["emoji_count"] == 2
    assert "😊" in res["emoji_vocabulary"]
    assert "🚀" in res["emoji_vocabulary"]
    assert "xD" in res["emoticons"]

def test_syntax():
    text = "The quick brown fox jumps over the lazy dog."
    res = pos_features(text)
    if res['status'] == 'success':
        assert res["noun_ratio"] > 0
        assert res["verb_ratio"] > 0
        assert res["adjective_ratio"] > 0
