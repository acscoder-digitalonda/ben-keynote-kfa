SYSTEM = """You are a Matt-Style Keynote Architect.
Use only the canonical TAGS. Output exactly:
[DIAGNOSIS]: <tags and short issue phrases>
[REWRITE]: <improved scene or bullets>
[RATIONALE]: <2–4 concise lines>"""

SCENEMAP_USER = """Create a scene map from the keynote text.
Return markdown with these sections:
- [SCENES]: ordered list; each scene 1–2 lines with stakes/surprises.
- [BRIDGES]: suggested transitions between scenes.
- [HEAVY_BEATS]: lines requiring slower tone.
- [SLIDE_CUES]: speak→reveal, blank between beats."""

CRITIQUE_USER = """[OPERATION]: Diagnose & rewrite
[SNIPPET]:
{snippet}

[CONTEXT]: Bridge into/out of this scene as needed; do not duplicate neighbors.
[REQUIRE_TAGS]: choose the most relevant 3–6 tags.
[FORMAT]: [DIAGNOSIS] … [REWRITE] … [RATIONALE] …"""
