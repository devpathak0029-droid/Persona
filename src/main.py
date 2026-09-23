from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from .models.post import Post
from .persona.profile_builder import build_profile

app = FastAPI(title="PRALAYX Persona Analysis")

class AnalyzeRequest(BaseModel):
    persona_id: str
    posts: list[Post]

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    return build_profile(req.persona_id, req.posts)

@app.get("/health")
def health():
    return {"status": "ok", "module": "persona-analysis"}
