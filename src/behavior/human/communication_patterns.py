import re
from typing import List, Dict, Any
from .models import HumanBehaviorSignal

SLANG_DICTIONARY = [
    "opsec", "dox", "fud", "shell", "botnet", "skid", "0day", 
    "pwn", "pwned", "rce", "c2", "rat", "crypter", "carding", "dump"
]

TECHNICAL_TERMS = [
    "buffer overflow", "sql injection", "xss", "cross-site scripting",
    "privilege escalation", "lateral movement", "payload", "rootkit",
    "ransomware", "command and control", "reverse shell"
]

def analyze_communication(cleaned_texts: List[str]) -> List[Dict[str, Any]]:
    """
    Analyze text to identify communication patterns like slang and technical terminology.
    Returns a list of HumanBehaviorSignal dictionaries.
    """
    signals = []
    
    slang_found = set()
    tech_found = set()
    
    # In a real implementation we would map these back to original evidence IDs,
    # but here we are just taking a list of strings as requested.
    
    for i, text in enumerate(cleaned_texts):
        text_lower = text.lower()
        
        # Check for slang
        for slang in SLANG_DICTIONARY:
            if re.search(r'\b' + re.escape(slang) + r'\b', text_lower):
                slang_found.add(slang)
                
        # Check for technical terminology
        for term in TECHNICAL_TERMS:
            if term in text_lower:
                tech_found.add(term)
                
    if slang_found:
        signal = HumanBehaviorSignal(
            category='communication',
            signal_type='SLANG_REUSE',
            observations=[f"Observed usage of domain-specific slang: {', '.join(slang_found)}"],
            evidence_ids=[],  # No direct mapping provided in basic signature
            confidence=0.75,
            explanation="Use of specific subcultural terminology indicates familiarity with domain norms.",
            limitations=["Slang may be widely adopted across different subgroups."]
        )
        signals.append(signal.model_dump())
        
    if tech_found:
        signal = HumanBehaviorSignal(
            category='communication',
            signal_type='TECHNICAL_VOCABULARY_REUSE',
            observations=[f"Observed usage of technical terminology: {', '.join(tech_found)}"],
            evidence_ids=[],
            confidence=0.85,
            explanation="Presence of technical vocabulary indicates domain knowledge or specific areas of interest.",
            limitations=["Terminology is common in broader security communities, not just specific actors."]
        )
        signals.append(signal.model_dump())

    return signals
