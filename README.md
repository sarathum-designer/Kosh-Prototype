# Kosh

India's GCC truth, in one place.

Kosh is a neutral record of India's Global Capability Centre ecosystem. A company planning an India centre describes its plan; Kosh compares cities, screens state incentives against the plan, shows where published numbers disagree, answers questions from sourced data only, and produces a one-page decision brief. Every number carries its source, date and definition.

This repository is the working prototype: API, database, ingestion pipeline, AI layer and front end.

**Live demo:** https://sarathum-designer.github.io/kosh/ (after the repo is renamed to kosh) (static build; the AI assistant falls back to stored figures there. Run the server below with an API key for the full assistant.)

## Run it

```bash
cd backend
pip install -r requirements.txt          # Flask only; everything else is the standard library
python -m kosh.app                       # http://localhost:8080
```

Optional:

```bash
export ANTHROPIC_API_KEY=...             # turns on "Ask Kosh", plan reading and brief writing
export KOSH_REVIEW_TOKEN=...             # protects analyst endpoints (default: dev-review-token)
export KOSH_DB=/path/to/kosh.db          # default: backend/kosh.db
```

Without an API key the product still works: costs, incentives, conflicts, providers and the brief are deterministic. The assistant falls back to showing the stored figures that match the question.

Tests:

```bash
cd backend && python -m unittest discover -s tests -v     # 26 tests
```

Docker:

```bash
docker build -t kosh . && docker run -p 8080:8080 -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY kosh
```

## What's where

| Path | What it is |
|---|---|
| `backend/schema.sql` | Data model: sources, facts, conflicts, states and rules, GCCs, providers, verified deliveries, plans, consented intros, audit log |
| `backend/kosh/db.py` | SQLite access, seeding, and the dataset the front end reads |
| `backend/kosh/engine.py` | Cost model, incentive screening, conflict detection. No AI; fully reproducible |
| `backend/kosh/assistant.py` | Retrieval, grounded prompting and citation verification |
| `backend/kosh/pipeline.py` | Ingestion: document to candidate facts to human review to published |
| `backend/kosh/app.py` | REST API and front-end server |
| `backend/tests/` | Unit and API tests |
| `frontend/index.html` | The product UI (same code as the hosted prototype) plus `shim.js` to run self-hosted |
| `data/kosh-data.json` | The curated seed dataset: 48 sources, 58 figures, 9 documented disagreements, 12 state policies |
| `data/build_data.py` | How the seed dataset is built, with integrity checks |
| `docs/` | Architecture, API, UX and data operations |
| `site/` | Static build of the front end, deployed to GitHub Pages |
| `brand/` | Kosh logo files, colour and type tokens, brand guidelines |

## Principles the code enforces

1. **No number without a source.** `facts.source_id` is required; the API never returns a pending fact.
2. **Disagreement is shown, not resolved silently.** New figures are checked against published ones; a gap above 10% opens a conflict for an analyst to explain.
3. **The AI cannot invent evidence.** It sees only retrieved facts, and any citation that doesn't exist is stripped and reported.
4. **Refuse rather than guess.** Cities without salary or rent data are not priced.
5. **Neutral by construction.** Providers are listed alphabetically; the paid `plan` column never touches ordering. Introductions require recorded consent per provider.
