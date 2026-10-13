"""Run from backend/:  python -m unittest discover -s tests -v"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kosh import assistant, db, engine, pipeline  # noqa: E402
from kosh.app import create_app  # noqa: E402

AUTH = {"Authorization": "Bearer dev-review-token"}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.app = create_app(self.tmp.name)
        self.client = self.app.test_client()
        self.conn = self.app.config["CONN"]
        self.ds = db.dataset(self.conn, self.app.config["ASSUMPTIONS"], self.app.config["META"])

    def tearDown(self):
        self.conn.close()
        os.unlink(self.tmp.name)


class DataIntegrity(Base):
    def test_every_fact_has_a_known_source_and_date(self):
        src = {s["id"] for s in self.ds["sources"]}
        for f in self.ds["facts"]:
            self.assertIn(f["source"], src, f["id"])
            self.assertTrue(f["as_of"], f["id"])

    def test_conflicts_point_at_real_facts(self):
        ids = {f["id"] for f in self.ds["facts"]}
        for x in self.ds["conflicts"]:
            self.assertGreaterEqual(len(x["facts"]), 2)
            self.assertTrue(set(x["facts"]) <= ids)

    def test_round_trip_matches_seed_file(self):
        seed = json.loads(db.DEFAULT_SEED.read_text())
        self.assertEqual(len(seed["facts"]), len(self.ds["facts"]))
        self.assertEqual(seed["facts"][0]["value"], self.ds["facts"][0]["value"])


class CostModel(Base):
    def test_bengaluru_known_values(self):
        p = engine.Plan.from_dict({"y1": 60, "y3": 150, "model": "eor", "cities": ["bengaluru"]})
        c = engine.cost_for(self.ds, "bengaluru", p)
        # 60 x 15.7 lakh x 1.125 = ₹10.5975 crore payroll
        self.assertAlmostEqual(c["payroll_cr"], 10.598, places=2)
        self.assertLess(c["low_cr"], c["high_cr"])

    def test_refuses_to_price_without_data(self):
        p = engine.Plan.from_dict({"y1": 40, "cities": ["kochi"]})
        self.assertIsNone(engine.cost_for(self.ds, "kochi", p))

    def test_bot_flags_unpublished_fees(self):
        p = engine.Plan.from_dict({"y1": 40, "model": "bot", "cities": ["pune"]})
        self.assertIn("BOT partner fees (unpublished)", engine.cost_for(self.ds, "pune", p)["excludes"])


class Incentives(Base):
    def state(self, sid):
        return next(s for s in self.ds["states"] if s["id"] == sid)

    def test_rajasthan_excludes_bot(self):
        p = engine.Plan.from_dict({"model": "bot", "y1": 300, "y3": 600})
        self.assertEqual(engine.screen_state(self.state("RJ"), p, None)["verdict"], "no")

    def test_odisha_needs_ranked_parent(self):
        p = engine.Plan.from_dict({"model": "own", "rank": "other", "y1": 100, "y3": 200})
        self.assertEqual(engine.screen_state(self.state("OD"), p, None)["verdict"], "no")
        p.rank = "g2000"
        self.assertNotEqual(engine.screen_state(self.state("OD"), p, None)["verdict"], "no")

    def test_gujarat_threshold_reached_in_year_three(self):
        p = engine.Plan.from_dict({"model": "own", "y1": 30, "y3": 80})
        r = engine.screen_state(self.state("GJ"), p, None)
        self.assertEqual(r["verdict"], "check")
        self.assertTrue(any("year 3" in x for x in r["reasons"]))

    def test_telangana_has_no_policy(self):
        self.assertEqual(engine.screen_state(self.state("TG"), engine.Plan(), "hyderabad")["verdict"], "none")

    def test_maharashtra_excludes_pure_bpo(self):
        p = engine.Plan.from_dict({"model": "own", "functions": ["support"]})
        self.assertEqual(engine.screen_state(self.state("MH"), p, "pune")["verdict"], "no")


class Conflicts(Base):
    def test_detects_gcc_count_disagreement(self):
        groups = engine.detect_conflicts(self.ds["facts"])
        india_counts = {f["id"] for f in self.ds["facts"] if f["subject"] == "india" and f["metric"] == "GCC count"}
        self.assertTrue(any(set(g) == india_counts for g in groups))

    def test_close_values_are_not_conflicts(self):
        fs = [dict(id="a", subject="x", metric="m", num=100), dict(id="b", subject="x", metric="m", num=105)]
        self.assertEqual(engine.detect_conflicts(fs), [])


class Assistant(Base):
    def test_strips_invented_citations(self):
        text, bad = assistant.verify_citations(self.ds, "There are 2,117 GCCs [F1, F999] and more [F777].")
        self.assertIn("[F1]", text)
        self.assertNotIn("F999", text)
        self.assertEqual(set(bad), {"F999", "F777"})

    def test_retrieval_finds_city_salary(self):
        ids = [f["metric"] for f in assistant.retrieve(self.ds, "engineer salary in Pune")]
        self.assertIn("Software engineer median salary", ids)

    def test_no_match_is_honest(self):
        r = assistant.answer(self.ds, "zzzz qqqq", model_fn=lambda p: "x")
        self.assertEqual(r["mode"], "no_match")

    def test_model_path_uses_only_retrieved_facts(self):
        seen = {}
        r = assistant.answer(self.ds, "How many GCCs in Bengaluru?", model_fn=lambda p: seen.setdefault("p", p) and "487 [F33]")
        self.assertIn("FACTS:", seen["p"])
        self.assertEqual(r["mode"], "model")


class Pipeline(Base):
    SRC = {"id": "S900", "publisher": "Test Wire", "title": "Pune GCC note", "url": "https://example.com/n", "date": "2026-10", "kind": "news"}

    def test_offline_extract_review_and_conflict(self):
        out = pipeline.ingest(self.conn, self.SRC, "Pune now hosts 260 GCCs, the state said.", "2026-10")
        self.assertEqual(len(out["pending_review"]), 1)
        fid = out["pending_review"][0]
        # pending facts never reach the public dataset
        ds = db.dataset(self.conn, self.app.config["ASSUMPTIONS"], self.app.config["META"])
        self.assertNotIn(fid, {f["id"] for f in ds["facts"]})
        res = pipeline.review(self.conn, fid, "published", "analyst@kosh")
        self.assertIsNotNone(res["conflict"])  # 260 vs Vestian's 178 for Pune

    def test_model_extraction_is_validated(self):
        fake = json.dumps([
            {"subject": "india", "metric": "GCC count", "value": 2200, "unit": "GCCs", "definition": "companies", "as_of": "2026-09", "quote": "2,200 GCCs"},
            {"subject": "atlantis", "metric": "GCC count", "value": 5, "unit": "GCCs", "as_of": "2026-09", "quote": "x"},
            {"subject": "india", "metric": "Vibes", "value": 1, "as_of": "2026-09", "quote": "y"},
        ])
        out = pipeline.ingest(self.conn, self.SRC, "doc", "2026-09", model_fn=lambda p: fake)
        self.assertEqual(len(out["pending_review"]), 1)
        self.assertEqual(len(out["rejected"]), 2)


class Api(Base):
    def test_health_and_dataset(self):
        self.assertTrue(self.client.get("/api/health").json["ok"])
        self.assertGreater(len(self.client.get("/api/dataset").json["facts"]), 50)

    def test_compare(self):
        r = self.client.post("/api/compare", json={"y1": 60, "y3": 150, "model": "eor", "cities": ["pune", "kochi"]}).json
        self.assertIsNotNone(r["cities"][0]["cost"])
        self.assertIsNone(r["cities"][1]["cost"])

    def test_providers_are_alphabetical(self):
        names = [p["name"] for p in self.client.get("/api/providers").json]
        self.assertEqual(names, sorted(names))

    def test_review_endpoints_need_auth(self):
        self.assertEqual(self.client.get("/api/review").status_code, 401)
        self.assertEqual(self.client.get("/api/review", headers=AUTH).status_code, 200)

    def test_intro_requires_consent(self):
        pid = self.client.post("/api/plans", json={"plan": {"y1": 20}}).json["id"]
        self.assertEqual(self.client.post("/api/intros", json={"plan_id": pid, "providers": ["ANSR"]}).status_code, 400)
        r = self.client.post("/api/intros", json={"plan_id": pid, "providers": ["ANSR"], "consent": "I agree to share my plan with ANSR."})
        self.assertEqual(r.status_code, 201)

    def test_index_injects_live_data(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertNotIn("/*__DATA__*/", html)
        self.assertIn('"facts":[', html)

    def test_ask_offline(self):
        os.environ.pop("ANTHROPIC_API_KEY", None)
        r = self.client.post("/api/ask", json={"question": "attrition in Chennai"}).json
        self.assertEqual(r["mode"], "offline")


if __name__ == "__main__":
    unittest.main()
