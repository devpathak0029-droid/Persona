from typing import List, Dict, Any
from .alias_behavior import analyze_aliases
from .communication_patterns import analyze_communication

def analyze_human_behavior(posts: List[Dict[str, Any]], cleaned_texts: List[str]) -> Dict[str, Any]:
    """
    Orchestrates the human-behavior analysis phase.
    Calls alias and communication pattern analyzers and returns a summarized dictionary of signals.
    """
    signals = []
    
    # 1. Analyze aliases
    alias_signals = analyze_aliases(posts)
    signals.extend(alias_signals)
    
    # 2. Analyze communication patterns
    comm_signals = analyze_communication(cleaned_texts)
    signals.extend(comm_signals)
    
    # Generate summary metrics
    signal_types = {}
    for sig in signals:
        stype = sig.get('signal_type', 'UNKNOWN')
        signal_types[stype] = signal_types.get(stype, 0) + 1
        
    summary_metrics = {
        'total_signals': len(signals),
        'signal_types_breakdown': signal_types,
        'categories_analyzed': ['identity', 'communication']
    }
    
    return {
        'signals': signals,
        'summary_metrics': summary_metrics
    }
