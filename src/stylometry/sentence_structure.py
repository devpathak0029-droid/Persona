import re
import statistics

def sentence_features(text: str) -> dict:
    # Split keeping delimiters to check sentence endings
    parts = re.split(r"([.!?]+)", text)
    
    sentences = []
    endings = []
    current_sentence = ""
    
    for i in range(0, len(parts)-1, 2):
        s = parts[i].strip()
        if s:
            sentences.append(s)
            endings.append(parts[i+1])
    
    # If the text doesn't end with punctuation, capture the last part
    if len(parts) % 2 != 0:
        s = parts[-1].strip()
        if s:
            sentences.append(s)
            endings.append("")

    lengths = [len(s.split()) for s in sentences]
    if not lengths:
        return {"sentence_count": 0}
        
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    median = statistics.median(lengths)
    
    num_questions = sum(1 for e in endings if '?' in e)
    num_exclamations = sum(1 for e in endings if '!' in e)
    
    total_sentences = len(sentences)
    
    imperative_words = {'do', "don't", 'use', 'try', 'check', 'go', 'make', 'let', 'get', 'send', 'buy', 'sell'}
    imperative_indicators = 0
    for s in sentences:
        words = s.lower().split()
        if words and words[0] in imperative_words:
            imperative_indicators += 1
            
    conjunctions = {'and', 'or', 'but', 'nor', 'yet', 'so', 'because', 'although', 'while', 'if', 'then', 'unless', 'until', 'whether'}
    total_conjunctions = sum(sum(1 for w in s.lower().split() if w in conjunctions) for s in sentences)
    conjunction_density = total_conjunctions / total_sentences
    
    return {
        "sentence_count": total_sentences,
        "mean_sentence_length": mean,
        "min_sentence_length": min(lengths),
        "max_sentence_length": max(lengths),
        "sentence_length_variance": variance,
        "median_sentence_length": float(median),
        "question_ratio": num_questions / total_sentences,
        "exclamation_ratio": num_exclamations / total_sentences,
        "imperative_indicators": imperative_indicators,
        "conjunction_density": conjunction_density
    }
