"""Deterministic engines: cost model, incentive screening, conflict detection.

These run without any AI so every number on screen can be reproduced and audited.
The front end implements the same rules; tests keep the two honest.
"""
from __future__ import annotations

from dataclasses import dataclass, field

MODELS = {"eor", "bot", "own"}
RANKS = {"g2000", "f1000", "other"}


@dataclass
class Plan:
    company: str = "My company"
    revenue: str = "100m-1b"
    rank: str = "other"
    functions: list = field(default_factory=lambda: ["engineering"])
    y1: int = 50
    y3: int = 100
    model: str = "eor"
    cities: list = field(default_factory=lambda: ["bengaluru"])
    timeline: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Plan":
        p = cls()
        for k in ("company", "revenue", "rank", "timeline"):
            if d.get(k):
                setattr(p, k, str(d[k]))
        if isinstance(d.get("functions"), list):
            p.functions = [str(x) for x in d["functions"]]
        if isinstance(d.get("cities"), list) and d["cities"]:
            p.cities = [str(x) for x in d["cities"]]
        p.y1 = max(1, int(d.get("y1") or p.y1))
        p.y3 = max(p.y1, int(d.get("y3") or p.y3))
        if d.get("model") in MODELS:
            p.model = d["model"]
        if d.get("rank") in RANKS:
            p.rank = d["rank"]
        return p


def _first(ds: dict, subject: str, metric: str):
    for f in ds["facts"]:
        if f["subject"] == subject and f["metric"] == metric:
            return f
    return None


def rent_for(ds: dict, city_id: str):
    a = ds["assumptions"]
    city = next((c for c in ds["cities"] if c["id"] == city_id), None)
    if city_id == "hyderabad":
        f = _first(ds, "hyderabad", "Office rent, SBD")
        return {"lo": 70, "hi": 95, "fact": f and f["id"]}
    if city_id == "bengaluru":
        f = _first(ds, "bengaluru", "Office rent (single transaction)")
        return {"lo": a["rent_fallback"]["low"], "hi": 113, "fact": f and f["id"]}
    if city and city["tier"] == 2:
        return None  # no defensible figure: refuse to price rather than guess
    f = _first(ds, "india", "Grade A office rent, tier-1 cities")
    return {"lo": a["rent_fallback"]["low"], "hi": a["rent_fallback"]["high"], "fact": f and f["id"]}


def cost_for(ds: dict, city_id: str, plan: Plan):
    """Year-one run cost in ₹ crore (low, high). None when the data cannot support a price."""
    a = ds["assumptions"]
    sal = _first(ds, city_id, "Software engineer median salary")
    rent = rent_for(ds, city_id)
    if not sal or not rent:
        return None
    heads = plan.y1
    payroll = heads * sal["num"] * (1 + a["statutory_load"]["value"]) / 100
    sqft = heads * a["sqft_per_seat"]["value"]
    rent_lo, rent_hi = sqft * rent["lo"] * 12 / 1e7, sqft * rent["hi"] * 12 / 1e7
    eor_lo = eor_hi = 0.0
    if plan.model == "eor":
        fx = a["inr_per_usd"]["value"]
        eor_lo, eor_hi = heads * 99 * 12 * fx / 1e7, heads * 599 * 12 * fx / 1e7
    return {
        "city": city_id, "salary_fact": sal["id"], "rent_fact": rent["fact"],
        "payroll_cr": round(payroll, 3), "rent_cr": [round(rent_lo, 3), round(rent_hi, 3)],
        "eor_cr": [round(eor_lo, 3), round(eor_hi, 3)],
        "low_cr": round(payroll + rent_lo + eor_lo, 3), "high_cr": round(payroll + rent_hi + eor_hi, 3),
        "excludes": ["fit-out", "IT", "recruitment fees", "travel"] + (["BOT partner fees (unpublished)"] if plan.model == "bot" else []),
    }


ORDER = {"likely": 0, "check": 1, "no": 2, "none": 3}


def screen_state(state: dict, plan: Plan, city_id: str | None) -> dict:
    """Screen a plan against a state's published GCC policy rules. Returns verdict + plain reasons."""
    r = state.get("rules", {})
    reasons: list[str] = []
    verdict = "likely"

    def down(v):
        nonlocal verdict
        if ORDER[v] > ORDER[verdict]:
            verdict = v

    if r.get("no_policy"):
        return {"state": state["id"], "verdict": "none", "reasons": ["No notified GCC policy to claim from today. " + state.get("watch", "")]}
    if r.get("ownership") and plan.model != "own":
        down("no"); reasons.append("Only wholly owned units qualify. Your plan uses " + ("a BOT partner." if plan.model == "bot" else "an EOR."))
    if r.get("min_employees"):
        m = r["min_employees"]
        if plan.y1 < m <= plan.y3:
            down("check"); reasons.append(f"Needs {m}+ employees. You reach that in year 3, not year 1.")
        elif plan.y3 < m:
            down("no"); reasons.append(f"Needs {m}+ employees; your plan stays below that.")
    if r.get("min_employees_noida"):
        th = r["min_employees_noida"] if city_id == "ncr" else r["min_employees_other"]
        if plan.y3 < th:
            down("check"); reasons.append(f"Needs {th} staff (or a capital threshold). Your year-3 plan is {plan.y3}.")
    if r.get("parent_rank") and plan.rank not in r["parent_rank"]:
        down("no"); reasons.append("Parent must be Fortune 1000 or Forbes G2000.")
    if r.get("excluded_functions"):
        bad = [f for f in plan.functions if f in ("support", "sales")]
        if bad:
            down("no" if len(bad) == len(plan.functions) else "check")
            reasons.append("BPO, call-centre and pure sales units are excluded.")
    if r.get("first_n"):
        down("check"); reasons.append(f"The richest incentives go to the first {r['first_n']} large GCCs. Ask how many slots are left.")
    if r.get("dated"):
        down("check"); reasons.append("Scheme figures date from Feb 2024 and run to Mar 2027. Confirm they still apply.")
    if state["id"] == "KA" and city_id == "bengaluru":
        reasons.append("The 'Beyond Bengaluru' package does not apply inside Bengaluru.")
    if plan.model == "eor" and verdict != "no":
        down("check"); reasons.append("On an EOR your staff sit on the provider's payroll; incentives are normally claimed by your own registered unit.")
    if "not verified" in state["status"] or "pending" in state["status"]:
        down("check"); reasons.append(state.get("watch", ""))
    reasons = list(dict.fromkeys(x for x in reasons if x))
    return {"state": state["id"], "verdict": verdict, "reasons": reasons or ["Your plan meets the published thresholds."]}


def detect_conflicts(facts: list[dict], tolerance: float = 0.10) -> list[list[str]]:
    """Group published facts that share subject+metric and whose numbers differ by more than `tolerance`.

    New figures from the ingestion pipeline pass through this, so a disagreement is surfaced
    to a reviewer the day it appears instead of silently overwriting an older number.
    """
    groups: dict[tuple, list[dict]] = {}
    for f in facts:
        if f.get("num") is None:
            continue
        groups.setdefault((f["subject"], f["metric"]), []).append(f)
    out = []
    for g in groups.values():
        if len(g) < 2:
            continue
        nums = [x["num"] for x in g]
        lo, hi = min(nums), max(nums)
        if lo == 0 or (hi - lo) / lo > tolerance:
            out.append([x["id"] for x in g])
    return out
