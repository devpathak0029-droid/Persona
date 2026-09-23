import os
import json

# This module uses an LLM (like Google Gemini) to perform deep semantic and psychological profiling
# of a threat actor's writing style, identifying traits that pure statistical stylometry might miss.

def generate_ai_profile(text_corpus: str) -> dict:
    """
    Uses an LLM to generate a deep behavioral and stylometric profile of the author.
    Requires GEMINI_API_KEY environment variable.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not configured. Skipping LLM stylistic analysis."}
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert threat intelligence analyst and forensic linguist.
        Analyze the following text corpus written by a single threat actor.
        Provide a detailed stylometric and behavioral profile in valid JSON format with the following keys:
        - "tone": (string) The general tone (e.g., Aggressive, Professional, Skiddie, Paranoid).
        - "opsec_awareness": (string) High/Medium/Low based on how they talk about security.
        - "native_language_hints": (string) Any signs of non-native English or regional idioms.
        - "common_slang": (list of strings) Dark web or hacker slang used.
        - "motivations": (list of strings) Apparent motivations (e.g., Financial, Ideological, Clout).
        - "persona_summary": (string) A 2-sentence summary of this actor's linguistic persona.
        
        Text Corpus:
        {text_corpus[:10000]} # Limit context window
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        return {"error": f"AI Profiling failed: {str(e)}"}
