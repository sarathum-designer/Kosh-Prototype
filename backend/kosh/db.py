"""SQLite access and seeding. Swap the connect() call for Postgres in production."""
import json
import os
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE.parent / "schema.sql"
DEFAULT_SEED = HERE.parent.parent / "data" / "kosh-data.json"


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text())
    conn.commit()


def seed(conn: sqlite3.Connection, seed_path: Path = DEFAULT_SEED) -> dict:
    """Load the curated dataset. Idempotent: existing rows are replaced."""
    data = json.loads(Path(seed_path).read_text())
    cur = conn.cursor()
    for s in data["sources"]:
        cur.execute(
            "INSERT OR REPLACE INTO sources(id,publisher,title,url,published_on,kind,sells_services) VALUES (?,?,?,?,?,?,?)",
            (s["id"], s["publisher"], s["title"], s["url"], s["date"], s["kind"], s.get("sells_services")),
        )
    for f in data["facts"]:
        cur.execute(
            "INSERT OR REPLACE INTO facts(id,subject,metric,value_text,value_num,unit,definition,as_of,source_id,note) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (f["id"], f["subject"], f["metric"], str(f["value"]), f.get("num"), f["unit"], f.get("definition", ""), f["as_of"], f["source"], f.get("note", "")),
        )
    for c in data["cities"]:
        cur.execute("INSERT OR REPLACE INTO cities(id,name,state_id,alt_state,tier) VALUES (?,?,?,?,?)",
                    (c["id"], c["name"], c["state"], c.get("alt_state"), c["tier"]))
    for s in data["states"]:
        cur.execute(
            "INSERT OR REPLACE INTO states(id,name,status,source_id,rules_json,incentives_json,watch) VALUES (?,?,?,?,?,?,?)",
            (s["id"], s["name"], s["status"], s["source"], json.dumps(s.get("rules", {})), json.dumps(s.get("incentives", [])), s.get("watch", "")),
        )
    cur.execute("DELETE FROM conflict_facts")
    for x in data["conflicts"]:
        cur.execute("INSERT OR REPLACE INTO conflicts(id,question,why) VALUES (?,?,?)", (x["id"], x["question"], x["why"]))
        for fid in x["facts"]:
            cur.execute("INSERT INTO conflict_facts(conflict_id,fact_id) VALUES (?,?)", (x["id"], fid))
    cur.execute("DELETE FROM gccs")
    for g in data["gccs"]:
        cur.execute("INSERT INTO gccs(name,sector,city_id,status,detail,source_id,as_of) VALUES (?,?,?,?,?,?,?)",
                    (g["name"], g["sector"], g["city"], g["status"], g["detail"], g["source"], g["as_of"]))
    for p in data["providers"]:
        cur.execute("INSERT OR REPLACE INTO providers(name,category,claim,source_id) VALUES (?,?,?,?)",
                    (p["name"], p["category"], p["claim"], p["source"]))
    conn.execute("INSERT INTO audit_log(actor,action,object,detail) VALUES ('system','seed','dataset',?)", (str(seed_path),))
    conn.commit()
    return {"sources": len(data["sources"]), "facts": len(data["facts"]), "assumptions": data["assumptions"], "meta": data["meta"]}


def dataset(conn: sqlite3.Connection, assumptions: dict, meta: dict) -> dict:
    """Rebuild the JSON shape the front end reads, from the database (published facts only)."""
    q = lambda sql, *a: [dict(r) for r in conn.execute(sql, a).fetchall()]
    sources = [dict(id=r["id"], publisher=r["publisher"], title=r["title"], url=r["url"], date=r["published_on"],
                    kind=r["kind"], sells_services=r["sells_services"]) for r in q("SELECT * FROM sources ORDER BY rowid")]
    facts = [dict(id=r["id"], subject=r["subject"], metric=r["metric"], value=_value(r), unit=r["unit"], num=r["value_num"],
                  source=r["source_id"], as_of=r["as_of"], definition=r["definition"], note=r["note"])
             for r in q("SELECT * FROM facts WHERE status='published' ORDER BY CAST(substr(id,2) AS INTEGER)")]
    cities = [dict(id=r["id"], name=r["name"], state=r["state_id"], tier=r["tier"], **({"alt_state": r["alt_state"]} if r["alt_state"] else {}))
              for r in q("SELECT * FROM cities ORDER BY rowid")]
    states = [dict(id=r["id"], name=r["name"], status=r["status"], source=r["source_id"], rules=json.loads(r["rules_json"]),
                   incentives=json.loads(r["incentives_json"]), watch=r["watch"]) for r in q("SELECT * FROM states ORDER BY rowid")]
    conflicts = []
    for x in q("SELECT * FROM conflicts ORDER BY CAST(substr(id,2) AS INTEGER)"):
        ids = [r["fact_id"] for r in q("SELECT fact_id FROM conflict_facts WHERE conflict_id=? ORDER BY CAST(substr(fact_id,2) AS INTEGER)", x["id"])]
        conflicts.append(dict(id=x["id"], question=x["question"], why=x["why"], facts=ids))
    gccs = [dict(name=r["name"], sector=r["sector"], city=r["city_id"], status=r["status"], detail=r["detail"], source=r["source_id"], as_of=r["as_of"])
            for r in q("SELECT * FROM gccs ORDER BY id")]
    providers = [dict(name=r["name"], category=r["category"], claim=r["claim"], source=r["source_id"],
                      verified_deliveries=r["verified"]) for r in q(
        "SELECT p.*, (SELECT COUNT(*) FROM deliveries d WHERE d.provider_id=p.id AND d.status='verified' AND d.public=1) AS verified FROM providers p ORDER BY p.name")]
    return dict(meta=meta, sources=sources, facts=facts, cities=cities, states=states, conflicts=conflicts, gccs=gccs, providers=providers, assumptions=assumptions)


def _value(r):
    v = r["value_text"]
    try:
        n = float(v)
        return int(n) if n.is_integer() else n
    except ValueError:
        return v


def default_path() -> str:
    return os.environ.get("KOSH_DB", str(HERE.parent / "kosh.db"))
