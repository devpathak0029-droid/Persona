"""PRALAYX Persona Analysis — FastAPI service."""
from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from .models.post import Post
from .persona.profile_builder import build_profile
from .persona.migration import detect_migration
from .comparison.pairwise import compare_profiles
from .comparison.matrix import build_similarity_matrix
from .comparison.ranking import rank_candidates
from .fusion.engine import fuse_signals
from .reports.json_report import generate_json_report
from .reports.html_report import generate_html_report
from .reports.pdf_report import generate_pdf_report

app = FastAPI(
    title="PRALAYX Persona Analysis",
    description="AI-based stylometric, semantic, and behavioral analysis module for dark web threat actor de-anonymization (SIH26151).",
    version="3.0.0",
)


# ── Request / Response Models ──────────────────────────────────────

class AnalyzeRequest(BaseModel):
    """Single-persona analysis request with optional PRALAYX IDs."""
    investigation_id: Optional[str] = None
    actor_id: Optional[str] = None
    run_id: Optional[str] = None
    session_id: Optional[str] = None
    persona_id: str
    posts: list[Post]


class CompareRequest(BaseModel):
    """Compare two or more personas."""
    investigation_id: Optional[str] = None
    personas: list[AnalyzeRequest] = Field(..., min_length=2)


class MigrationRequest(BaseModel):
    """Check migration hypothesis between two personas."""
    investigation_id: Optional[str] = None
    persona_a: AnalyzeRequest
    persona_b: AnalyzeRequest


# ── Endpoints ──────────────────────────────────────────────────────

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Build a complete persona profile from a corpus of posts."""
    return build_profile(
        persona_id=req.persona_id,
        posts=req.posts,
        investigation_id=req.investigation_id,
        actor_id=req.actor_id,
        run_id=req.run_id,
        session_id=req.session_id,
    )


@app.post("/compare")
def compare(req: CompareRequest):
    """Compare multiple personas and return similarity matrix + rankings."""
    profiles = []
    for p in req.personas:
        profile = build_profile(
            persona_id=p.persona_id,
            posts=p.posts,
            investigation_id=req.investigation_id,
            actor_id=p.actor_id,
            run_id=p.run_id,
            session_id=p.session_id,
        )
        profiles.append(profile)

    # Build similarity matrix
    matrix = build_similarity_matrix(profiles)

    # Build pairwise comparisons
    comparisons = []
    for i in range(len(profiles)):
        for j in range(i + 1, len(profiles)):
            comp = compare_profiles(profiles[i], profiles[j])
            comparisons.append(comp)

    # Rank all against the first persona
    rankings = []
    if len(profiles) >= 2:
        rankings = rank_candidates(profiles[0], profiles[1:])

    return {
        "investigation_id": req.investigation_id,
        "profiles": profiles,
        "comparisons": comparisons,
        "similarity_matrix": matrix,
        "rankings": rankings,
    }


@app.post("/migration")
def migration(req: MigrationRequest):
    """Check migration hypothesis between two personas."""
    profile_a = build_profile(
        persona_id=req.persona_a.persona_id,
        posts=req.persona_a.posts,
        investigation_id=req.investigation_id,
    )
    profile_b = build_profile(
        persona_id=req.persona_b.persona_id,
        posts=req.persona_b.posts,
        investigation_id=req.investigation_id,
    )
    result = detect_migration(
        profile_a, profile_b,
        posts_a=req.persona_a.posts,
        posts_b=req.persona_b.posts,
    )
    return {
        "investigation_id": req.investigation_id,
        "profile_a": profile_a,
        "profile_b": profile_b,
        "migration": result,
    }


@app.post("/report/{fmt}")
def report(fmt: str, req: AnalyzeRequest):
    """Generate a report in json, html, or pdf format."""
    profile = build_profile(
        persona_id=req.persona_id,
        posts=req.posts,
        investigation_id=req.investigation_id,
        actor_id=req.actor_id,
    )
    metadata = {
        "investigation_id": req.investigation_id,
        "actor_id": req.actor_id,
        "persona_id": req.persona_id,
        "generated_at": datetime.utcnow().isoformat(),
    }

    report_data = generate_json_report(profile, metadata=metadata)

    if fmt == "json":
        return report_data
    elif fmt == "html":
        html = generate_html_report(report_data)
        return HTMLResponse(content=html)
    elif fmt == "pdf":
        pdf_bytes = generate_pdf_report(report_data)
        if pdf_bytes:
            return Response(content=pdf_bytes, media_type="application/pdf",
                            headers={"Content-Disposition": "attachment; filename=persona_report.pdf"})
        return {"error": "PDF generation requires reportlab. Install with: pip install reportlab"}
    else:
        return {"error": f"Unsupported format: {fmt}. Use json, html, or pdf."}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "module": "persona-analysis", "version": "3.0.0"}
