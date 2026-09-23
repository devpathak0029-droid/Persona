# PRALAYX Persona Analysis

Persona, stylometry, semantic and behavioral analysis module for SIH26151.

## Scope

This module analyzes observable linguistic and behavioral patterns. It does not diagnose personality or claim identity from stylometry alone.

## Run

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8010
```

## API

POST `/analyze`

Example:

```json
{
  "persona_id": "PERS-001",
  "posts": [
    {
      "post_id": "p1",
      "author_id": "actor-a",
      "platform": "forum",
      "text": "Example post",
      "timestamp": "2026-09-01T12:00:00Z",
      "source_url": "https://example.invalid/post/1"
    }
  ]
}
```
