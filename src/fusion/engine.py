from typing import Dict, Any, List, Optional

def fuse_signals(signals: Dict[str, float], external_evidence: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Explainable signal fusion engine.
    """
    default_weights = {
        'style_similarity': 0.30,
        'semantic_similarity': 0.25,
        'behavioral_association': 0.20,
        'topic_similarity': 0.15,
        'temporal_association': 0.10
    }
    
    weighted_sum = 0.0
    weight_total = 0.0
    
    used_weights = {}
    limitations = [
        "Signal fusion provides analytical confidence, not identity verification.",
        "Weak individual signals should not be amplified by fusion."
    ]
    
    weak_signals = []
    
    for signal_name, value in signals.items():
        if signal_name in default_weights:
            weight = default_weights[signal_name]
            used_weights[signal_name] = weight
            weighted_sum += value * weight
            weight_total += weight
            
            if value < 0.3:
                weak_signals.append(signal_name)
                limitations.append(f"{signal_name} is weak ({value:.2f}) and should be interpreted cautiously")
                
    if weight_total > 0:
        combined_confidence = weighted_sum / weight_total
    else:
        combined_confidence = 0.0
        
    if combined_confidence < 0.3:
        confidence_band = 'LOW'
    elif combined_confidence <= 0.5:
        confidence_band = 'MODERATE'
    elif combined_confidence <= 0.7:
        confidence_band = 'SIGNIFICANT'
    elif combined_confidence <= 0.85:
        confidence_band = 'HIGH'
    else:
        confidence_band = 'VERY_HIGH'
        
    if combined_confidence > 0.7 and weak_signals:
        for ws in weak_signals:
            limitations.append(f"High combined confidence despite weak {ws}; interpret with caution")
            
    explanation_parts = [f"{k}={v:.2f}" for k, v in signals.items()]
    explanation = f"Combined confidence of {combined_confidence:.2f} ({confidence_band}) based on: " + ", ".join(explanation_parts)
    
    return {
        'signals': signals,
        'weights': used_weights,
        'combined_confidence': combined_confidence,
        'confidence_band': confidence_band,
        'explanation': explanation,
        'evidence_ids': [ev.get('evidence_id') for ev in (external_evidence or []) if 'evidence_id' in ev],
        'limitations': limitations
    }
