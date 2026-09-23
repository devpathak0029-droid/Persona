import os
import json
from typing import Dict, Any

def generate_ai_profile(text_corpus: str) -> Dict[str, Any]:
    """
    Generate an AI linguistic profile based on observable linguistic characteristics.
    Requires GEMINI_API_KEY environment variable.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return {
            'status': 'NOT_CONFIGURED',
            'provider': 'gemini',
            'message': 'GEMINI_API_KEY not set. Classical analysis continues without AI augmentation.'
        }
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Analyze the following text corpus and identify OBSERVABLE LINGUISTIC characteristics.
        DO NOT provide any psychological diagnosis, personality types, or statements on motivation.
        Focus strictly on writing style, vocabulary, and observable patterns.

        Return a JSON object with the following schema:
        - communication_style: string (e.g., 'formal', 'informal', 'technical', 'conversational')
        - formality: string ('high', 'medium', 'low')
        - technical_language: list of strings (technical terms observed)
        - recurring_terms: list of strings (frequently repeated words/phrases)
        - slang: list of strings (slang/colloquial terms observed)
        - language_hints: list of strings (signs of non-native English, regional expressions)
        - writing_patterns: list of strings (observable patterns like 'uses all caps for emphasis', 'frequent ellipsis')
        - observable_opsec_language: list of strings (security-related terminology used)
        - topic_preferences: list of strings (topics frequently discussed)
        - summary: string (2-sentence factual summary of observable writing characteristics)
        
        TEXT CORPUS:
        {text_corpus[:30000]}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        if not response.text:
            raise ValueError("Empty response from API.")
            
        result = json.loads(response.text)
        result['status'] = 'SUCCESS'
        result['provider'] = 'gemini'
        return result
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'provider': 'gemini',
            'message': str(e)
        }
