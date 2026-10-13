"""Grounded Q&A: retrieve facts, ask the model, then verify every citation.

The model never gets the open web. It gets the retrieved facts plus the user's plan,
and anything it cites must exist in the dataset or the citation is stripped and flagged.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("KOSH_MODEL", "claude-sonnet-5-5")

RULES = """You are Kosh, a neutral record of India's GCC ecosystem. Answer ONLY from the facts given.
- Follow every figure with its fact id in square brackets, e.g. [F12]. Cite a disagreement as [X3].
- When sources disagree, give the range and the reason. Never pick a winner silently.
- If the facts don't answer the question, say Kosh has no verified figure and name the kind of source that would settle it.
- Never rank, recommend or praise a service provider.
- Plain words, short sentences, at most 170 words."""

STOP = set("the a an of in on for to and or is are what how much many which who does do with by at from be it my our we i you".split())


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}


def retrieve(ds: dict, question: str, k: int = 24) -> list[dict]:
    """Keyword scoring over facts (metric, subject, city name, definition). Swap for embeddings at scale."""
    names = {c["id"]: c["name"].lower() for c in ds["cities"]}
    q = tokens(question)
    scored = []
    for f in ds["facts"]:
        hay = tokens(" ".join([f["metric"], f["subject"], names.get(f["subject"], ""), f.get("definition", ""), f["unit"]]))
        s = len(q & hay)
        if s:
            scored.append((s, f))
    scored.sort(key=lambda t: -t[0])
    return [f for _, f in scored[:k]]


def build_prompt(ds: dict, question: str, plan_summary: str = "") -> tuple[str, list[dict]]:
    facts = retrieve(ds, question)
    fids = {f["id"] for f in facts}
    conflicts = [x for x in ds["conflicts"] if fids & set(x["facts"])]
    src = {s["id"]: s for s in ds["sources"]}
    lines = [f'{f["id"]} | {f["subject"]} | {f["metric"]} | {f["value"]} {f["unit"]} | {src[f["source"]]["publisher"]}, {f["as_of"]}'
             + (f' | counts: {f["definition"]}' if f.get("definition") else "")
             + (f' | source sells: {src[f["source"]]["sells_services"]}' if src[f["source"]].get("sells_services") else "")
             for f in facts]
    xs = [f'{x["id"]}: {x["question"]} facts={",".join(x["facts"])} why: {x["why"]}' for x in conflicts]
    prompt = f"{RULES}\n\nFACTS:\n" + ("\n".join(lines) or "(none matched)") + "\n\nDISAGREEMENTS:\n" + ("\n".join(xs) or "(none)")
    if plan_summary:
        prompt += f"\n\nUSER'S PLAN:\n{plan_summary}"
    prompt += f"\n\nQUESTION: {question}"
    return prompt, facts


CITE = re.compile(r"\[((?:F|X|S)\d+(?:\s*,\s*(?:F|X|S)\d+)*)\]")


def verify_citations(ds: dict, text: str) -> tuple[str, list[str]]:
    """Remove citations that point at nothing; report them so the UI can warn."""
    valid = {f["id"] for f in ds["facts"]} | {x["id"] for x in ds["conflicts"]} | {s["id"] for s in ds["sources"]}
    bad: list[str] = []

    def fix(m):
        ids = [i.strip() for i in m.group(1).split(",")]
        keep = [i for i in ids if i in valid]
        bad.extend(i for i in ids if i not in valid)
        return "[" + ", ".join(keep) + "]" if keep else ""

    return CITE.sub(fix, text), bad


def call_model(prompt: str, api_key: str, max_tokens: int = 700) -> str:
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "content-type": "application/json", "x-api-key": api_key, "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def answer(ds: dict, question: str, plan_summary: str = "", api_key: str | None = None, model_fn=None) -> dict:
    prompt, facts = build_prompt(ds, question, plan_summary)
    if not facts:
        return {"answer": "Kosh has no verified figure that matches this question yet.", "facts": [], "mode": "no_match", "dropped_citations": []}
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if model_fn is None and not key:
        lines = [f'- {f["metric"]} ({f["subject"]}): {f["value"]} {f["unit"]} [{f["id"]}]' for f in facts[:6]]
        return {"answer": "The assistant is offline. Matching figures:\n" + "\n".join(lines), "facts": [f["id"] for f in facts], "mode": "offline", "dropped_citations": []}
    raw = model_fn(prompt) if model_fn else call_model(prompt, key)
    text, bad = verify_citations(ds, raw)
    return {"answer": text, "facts": [f["id"] for f in facts], "mode": "model", "dropped_citations": bad}
