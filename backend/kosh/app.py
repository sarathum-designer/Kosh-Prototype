"""Kosh API (Flask). Run:  python -m kosh.app   then open http://localhost:8080"""
from __future__ import annotations

import json
import os
from functools import wraps
from pathlib import Path

from flask import Flask, abort, jsonify, request

from . import assistant, db, engine, pipeline

FRONTEND = Path(__file__).resolve().parents[2] / "frontend"


def create_app(db_path: str | None = None, seed: bool = True) -> Flask:
    app = Flask(__name__)
    conn = db.connect(db_path or db.default_path())
    db.init(conn)
    info = db.seed(conn) if seed else {"assumptions": {}, "meta": {}}
    app.config.update(CONN=conn, ASSUMPTIONS=info["assumptions"], META=info["meta"],
                      REVIEW_TOKEN=os.environ.get("KOSH_REVIEW_TOKEN", "dev-review-token"))

    def ds():
        return db.dataset(conn, app.config["ASSUMPTIONS"], app.config["META"])

    def reviewer_only(fn):
        @wraps(fn)
        def wrap(*a, **k):
            if request.headers.get("Authorization") != "Bearer " + app.config["REVIEW_TOKEN"]:
                abort(401)
            return fn(*a, **k)
        return wrap

    @app.after_request
    def headers(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp

    @app.get("/api/health")
    def health():
        return {"ok": True, "facts": conn.execute("SELECT COUNT(*) FROM facts WHERE status='published'").fetchone()[0]}

    @app.get("/api/dataset")
    def dataset():
        return jsonify(ds())

    @app.get("/api/facts")
    def facts():
        d = ds()
        subject, metric = request.args.get("subject"), request.args.get("metric")
        out = [f for f in d["facts"] if (not subject or f["subject"] == subject) and (not metric or f["metric"] == metric)]
        return jsonify(out)

    @app.get("/api/facts/<fid>")
    def fact(fid):
        d = ds()
        f = next((x for x in d["facts"] if x["id"] == fid), None)
        if not f:
            abort(404)
        src = next(s for s in d["sources"] if s["id"] == f["source"])
        conflicts = [x["id"] for x in d["conflicts"] if fid in x["facts"]]
        return {"fact": f, "source": src, "conflicts": conflicts}

    @app.get("/api/conflicts")
    def conflicts():
        return jsonify(ds()["conflicts"])

    @app.get("/api/providers")
    def providers():
        cat = request.args.get("category")
        return jsonify([p for p in ds()["providers"] if not cat or p["category"] == cat])  # always alphabetical

    @app.post("/api/compare")
    def compare():
        d = ds()
        plan = engine.Plan.from_dict(request.get_json(force=True) or {})
        rows = []
        for cid in plan.cities:
            city = next((c for c in d["cities"] if c["id"] == cid), None)
            if not city:
                continue
            states = [s for s in d["states"] if s["id"] in (city["state"], city.get("alt_state"))]
            rows.append({"city": cid, "cost": engine.cost_for(d, cid, plan),
                         "incentives": [engine.screen_state(s, plan, cid) for s in states]})
        return {"plan": plan.__dict__, "cities": rows}

    @app.post("/api/ask")
    def ask():
        body = request.get_json(force=True) or {}
        q = str(body.get("question", "")).strip()[:1000]
        if not q:
            abort(400)
        return assistant.answer(ds(), q, str(body.get("plan_summary", ""))[:4000])

    @app.post("/api/sample")
    def sample():
        """Server-side stand-in for the artifact's `claude.use('sample')`, so the same front end runs self-hosted."""
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            return {"error": "not_granted", "message": "Set ANTHROPIC_API_KEY to enable the assistant."}, 503
        body = request.get_json(force=True) or {}
        inp = body.get("input")
        prompt = inp if isinstance(inp, str) else "\n\n".join(f'{m["role"].upper()}: {m["content"]}' for m in inp or [])
        if len(prompt.encode()) > 65536:
            return {"error": "prompt_too_large"}, 413
        text = assistant.call_model(prompt, key)
        clean, bad = assistant.verify_citations(ds(), text)
        return {"text": clean, "truncated": False, "dropped_citations": bad}

    @app.post("/api/plans")
    def save_plan():
        body = request.get_json(force=True) or {}
        plan = engine.Plan.from_dict(body.get("plan", {}))
        cur = conn.execute("INSERT INTO plans(owner_email,body_json) VALUES (?,?)", (body.get("email"), json.dumps(plan.__dict__)))
        conn.commit()
        return {"id": cur.lastrowid}, 201

    @app.post("/api/intros")
    def intros():
        """Share a plan with chosen providers. Requires explicit consent text, recorded per provider."""
        body = request.get_json(force=True) or {}
        consent = str(body.get("consent", "")).strip()
        if not consent:
            return {"error": "consent required"}, 400
        plan_id = int(body.get("plan_id", 0))
        if not conn.execute("SELECT 1 FROM plans WHERE id=?", (plan_id,)).fetchone():
            abort(404)
        ids = []
        for name in body.get("providers", []):
            p = conn.execute("SELECT id FROM providers WHERE name=?", (name,)).fetchone()
            if p:
                cur = conn.execute("INSERT INTO intro_requests(plan_id,provider_id,consent_text) VALUES (?,?,?)", (plan_id, p[0], consent))
                ids.append(cur.lastrowid)
        conn.commit()
        return {"intro_requests": ids, "status": "pending"}, 201

    # ---- analyst / reviewer endpoints ----
    @app.post("/api/ingest")
    @reviewer_only
    def ingest():
        body = request.get_json(force=True) or {}
        return pipeline.ingest(conn, body["source"], body["text"], body.get("as_of", ""), api_key=os.environ.get("ANTHROPIC_API_KEY"))

    @app.get("/api/review")
    @reviewer_only
    def review_queue():
        rows = conn.execute("SELECT * FROM facts WHERE status='pending_review' ORDER BY created_at").fetchall()
        return jsonify([dict(r) for r in rows])

    @app.post("/api/review/<fid>")
    @reviewer_only
    def review(fid):
        body = request.get_json(force=True) or {}
        try:
            return pipeline.review(conn, fid, body.get("decision", ""), body.get("reviewer", "analyst"))
        except ValueError as e:
            return {"error": str(e)}, 400

    @app.get("/")
    def index():
        """Serve the front end with the live, reviewed dataset injected (approved facts appear immediately)."""
        html = (FRONTEND / "index.html").read_text()
        data = json.dumps(ds(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return html.replace("/*__DATA__*/", data), 200, {"Content-Type": "text/html; charset=utf-8"}

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
