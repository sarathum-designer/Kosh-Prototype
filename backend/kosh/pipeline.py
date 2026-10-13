"""Ingestion: turn a scattered public document into reviewable facts.

    document (press release, policy PDF text, broker note)
      -> extract candidate facts (LLM with a strict JSON schema; regex fallback offline)
      -> validate (number, unit, date, subject, metric from the controlled list)
      -> store as status='pending_review' with extracted_by='pipeline:<model>'
      -> conflict check against published facts
      -> human reviewer approves / rejects (only approved facts are ever shown)
"""
from __future__ import annotations

import json
import re
import sqlite3

from . import assistant
from .engine import detect_conflicts

METRICS = [
    "GCC count", "GCC units", "GCC headcount", "GCC revenue", "New GCCs per year", "GCC attrition 2025",
    "GCC share of office leasing", "Software engineer median salary", "Office rent, SBD", "New GCCs in 2025-26",
]

EXTRACT_PROMPT = """Extract quantitative facts about India's Global Capability Centres from the document.
Return only a JSON array. Each item: {"subject": "india" or a city id from [%s],
"metric": one of %s, "value": number, "unit": string, "definition": what is counted (companies, units, ...),
"as_of": "YYYY-MM", "quote": the exact phrase (max 20 words) the number comes from}.
Skip anything not stated explicitly. If nothing qualifies, return [].

DOCUMENT:
%s"""


def extract_offline(text: str, cities: list[str]) -> list[dict]:
    """Very small rule-based extractor so the pipeline runs without a model (demo and tests)."""
    out = []
    t = text.lower()
    subject = next((c for c in cities if c in t), "india")
    m = re.search(r"(\d[\d,]*)\s*\+?\s*(gccs|global capability cent(?:re|er)s)", t)
    if m:
        out.append({"subject": subject, "metric": "GCC count", "value": float(m.group(1).replace(",", "")), "unit": "GCCs",
                    "definition": "As stated in the document", "as_of": "", "quote": m.group(0)})
    m = re.search(r"attrition[^.]{0,40}?(\d+(?:\.\d+)?)\s*%", t)
    if m:
        out.append({"subject": subject, "metric": "GCC attrition 2025", "value": float(m.group(1)), "unit": "%",
                    "definition": "As stated in the document", "as_of": "", "quote": m.group(0)})
    return out


def validate(c: dict, cities: list[str]) -> list[str]:
    errs = []
    if c.get("subject") not in (["india"] + cities):
        errs.append("unknown subject")
    if c.get("metric") not in METRICS:
        errs.append("metric not in controlled list")
    try:
        v = float(c.get("value"))
        if v < 0:
            errs.append("negative value")
    except (TypeError, ValueError):
        errs.append("value is not a number")
    if c.get("as_of") and not re.fullmatch(r"\d{4}(-\d{2})?(-\d{2})?", str(c["as_of"])):
        errs.append("bad as_of date")
    if not c.get("quote"):
        errs.append("no supporting quote")
    return errs


def next_fact_id(conn: sqlite3.Connection) -> str:
    n = conn.execute("SELECT COALESCE(MAX(CAST(substr(id,2) AS INTEGER)),0) FROM facts").fetchone()[0]
    return f"F{n + 1}"


def ingest(conn: sqlite3.Connection, source: dict, text: str, as_of: str, model_fn=None, api_key: str | None = None) -> dict:
    """Run one document through the pipeline. `source` is a dict for the sources table."""
    cities = [r[0] for r in conn.execute("SELECT id FROM cities")]
    if model_fn or api_key:
        prompt = EXTRACT_PROMPT % (", ".join(cities), json.dumps(METRICS), text[:20000])
        raw = model_fn(prompt) if model_fn else assistant.call_model(prompt, api_key, max_tokens=1500)
        m = re.search(r"\[.*\]", raw, re.S)
        candidates = json.loads(m.group(0)) if m else []
        extractor = "pipeline:" + assistant.MODEL
    else:
        candidates = extract_offline(text, cities)
        extractor = "pipeline:rules"

    conn.execute("INSERT OR IGNORE INTO sources(id,publisher,title,url,published_on,kind,sells_services) VALUES (?,?,?,?,?,?,?)",
                 (source["id"], source["publisher"], source["title"], source["url"], source["date"], source["kind"], source.get("sells_services")))
    accepted, rejected = [], []
    for c in candidates:
        errs = validate(c, cities)
        if errs:
            rejected.append({"candidate": c, "errors": errs})
            continue
        fid = next_fact_id(conn)
        conn.execute(
            "INSERT INTO facts(id,subject,metric,value_text,value_num,unit,definition,as_of,source_id,status,extracted_by,note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (fid, c["subject"], c["metric"], str(c["value"]), float(c["value"]), c.get("unit", ""), c.get("definition", ""),
             c.get("as_of") or as_of, source["id"], "pending_review", extractor, "quote: " + c["quote"]))
        accepted.append(fid)
    conn.execute("INSERT INTO audit_log(actor,action,object,detail) VALUES (?,?,?,?)",
                 (extractor, "ingest", source["id"], json.dumps({"accepted": accepted, "rejected": len(rejected)})))
    conn.commit()
    return {"pending_review": accepted, "rejected": rejected, "extractor": extractor}


def review(conn: sqlite3.Connection, fact_id: str, decision: str, reviewer: str) -> dict:
    """Approve or reject a pending fact. Approval runs conflict detection against published facts."""
    if decision not in ("published", "rejected"):
        raise ValueError("decision must be 'published' or 'rejected'")
    row = conn.execute("SELECT * FROM facts WHERE id=?", (fact_id,)).fetchone()
    if not row or row["status"] != "pending_review":
        raise ValueError("fact is not pending review")
    conn.execute("UPDATE facts SET status=?, reviewed_by=? WHERE id=?", (decision, reviewer, fact_id))
    conn.execute("INSERT INTO audit_log(actor,action,object) VALUES (?,?,?)", (reviewer, "review:" + decision, fact_id))
    new_conflict = None
    if decision == "published":
        same = [dict(id=r["id"], subject=r["subject"], metric=r["metric"], num=r["value_num"]) for r in conn.execute(
            "SELECT * FROM facts WHERE status='published' AND subject=? AND metric=?", (row["subject"], row["metric"]))]
        groups = detect_conflicts(same)
        if groups and fact_id in groups[0]:
            existing = conn.execute("SELECT conflict_id FROM conflict_facts WHERE fact_id IN (%s) LIMIT 1" % ",".join("?" * len(groups[0])), groups[0]).fetchone()
            if existing:
                new_conflict = existing[0]
            else:
                n = conn.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0]
                new_conflict = f"X{n + 1}"
                conn.execute("INSERT INTO conflicts(id,question,why) VALUES (?,?,?)",
                             (new_conflict, f'{row["metric"]} ({row["subject"]})', "Needs an analyst explanation."))
            for fid in groups[0]:
                conn.execute("INSERT OR IGNORE INTO conflict_facts(conflict_id,fact_id) VALUES (?,?)", (new_conflict, fid))
    conn.commit()
    return {"fact": fact_id, "status": decision, "conflict": new_conflict}
