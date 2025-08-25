# Keynote KFA (Keynote Feedback Guy) — Skeleton Repo

A plug-and-play tool to critique and rewrite keynotes in Matt-style with canonical tags.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
cp config.example.yaml config.yaml
# edit config.yaml to pick models

# Run on a sample keynote
python -m kfa.cli --input ./data/examples/keynote_sample.txt

# Optional: run server
uvicorn kfa.server:app --reload --port 8080
```
Outputs will appear in `./out/keynote_kfa.md` and `./out/keynote_kfa_notes.csv`.


## DOCX / SRT Ingestion
- `.docx` is supported via **python-docx** (already in requirements). We extract paragraphs and join them with blank lines.
- `.srt` subtitles are parsed naively: numeric indices and timestamp lines are skipped; caption text is joined with paragraph breaks.

## Web UI (FastAPI)
```bash
uvicorn kfa.server:app --reload --port 8080
# open http://localhost:8080
# upload a .txt/.md/.docx/.srt, choose chunk strategy, view preview and download outputs
```
