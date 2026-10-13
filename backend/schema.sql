-- Kosh data model (SQLite for the prototype; the same shape ports to Postgres).
-- Principle: a number is never stored without its source, date and definition.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
  id              TEXT PRIMARY KEY,           -- S1, S2 ...
  publisher       TEXT NOT NULL,
  title           TEXT NOT NULL,
  url             TEXT NOT NULL,
  published_on    TEXT NOT NULL,              -- ISO date or YYYY-MM
  kind            TEXT NOT NULL CHECK (kind IN ('research','news','government','broker','staffing','advisory','legal','registry','survey','talent','vendor','press release')),
  sells_services  TEXT,                       -- interest to declare; NULL when none known
  retrieved_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS facts (
  id           TEXT PRIMARY KEY,              -- F1, F2 ...
  subject      TEXT NOT NULL,                 -- 'india' or a city id
  metric       TEXT NOT NULL,
  value_text   TEXT NOT NULL,                 -- exactly as the source states it
  value_num    REAL,                          -- normalised number when one exists
  unit         TEXT NOT NULL DEFAULT '',
  definition   TEXT NOT NULL DEFAULT '',      -- what is being counted (companies vs units ...)
  as_of        TEXT NOT NULL,
  source_id    TEXT NOT NULL REFERENCES sources(id),
  status       TEXT NOT NULL DEFAULT 'published' CHECK (status IN ('pending_review','published','rejected','superseded')),
  extracted_by TEXT NOT NULL DEFAULT 'analyst', -- analyst | pipeline:<model>
  reviewed_by  TEXT,
  note         TEXT NOT NULL DEFAULT '',
  created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS facts_subject_metric ON facts(subject, metric);

CREATE TABLE IF NOT EXISTS conflicts (
  id        TEXT PRIMARY KEY,                 -- X1 ...
  question  TEXT NOT NULL,
  why       TEXT NOT NULL                     -- the human explanation of the gap
);
CREATE TABLE IF NOT EXISTS conflict_facts (
  conflict_id TEXT NOT NULL REFERENCES conflicts(id) ON DELETE CASCADE,
  fact_id     TEXT NOT NULL REFERENCES facts(id),
  PRIMARY KEY (conflict_id, fact_id)
);

CREATE TABLE IF NOT EXISTS cities (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  state_id   TEXT NOT NULL,
  alt_state  TEXT,
  tier       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS states (
  id          TEXT PRIMARY KEY,               -- KA, MH ...
  name        TEXT NOT NULL,
  status      TEXT NOT NULL,
  source_id   TEXT NOT NULL REFERENCES sources(id),
  rules_json  TEXT NOT NULL DEFAULT '{}',     -- machine-checkable eligibility rules
  incentives_json TEXT NOT NULL DEFAULT '[]',
  watch       TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS gccs (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  sector     TEXT,
  city_id    TEXT REFERENCES cities(id),
  status     TEXT NOT NULL,                   -- Announced | Expanding | Leased | Operating
  detail     TEXT,
  source_id  TEXT NOT NULL REFERENCES sources(id),
  as_of      TEXT NOT NULL,
  cin        TEXT                             -- MCA company id once matched
);

CREATE TABLE IF NOT EXISTS providers (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL UNIQUE,
  category   TEXT NOT NULL,
  claim      TEXT NOT NULL,                   -- what the provider says about itself
  source_id  TEXT NOT NULL REFERENCES sources(id),
  plan       TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free','verified','pro'))  -- paid tiers never change ordering
);

-- A delivery counts only when the client confirms it AND a document backs it.
CREATE TABLE IF NOT EXISTS deliveries (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_id     INTEGER NOT NULL REFERENCES providers(id),
  client_name     TEXT NOT NULL,
  scope           TEXT NOT NULL,
  started_on      TEXT,
  completed_on    TEXT,
  client_confirmed_at TEXT,
  evidence_kind   TEXT CHECK (evidence_kind IN ('contract_extract','mca_filing','lease_record','client_letter')),
  public          INTEGER NOT NULL DEFAULT 0,  -- client permission to show
  status          TEXT NOT NULL DEFAULT 'claimed' CHECK (status IN ('claimed','client_confirmed','verified','disputed'))
);

CREATE TABLE IF NOT EXISTS plans (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_email TEXT,
  body_json   TEXT NOT NULL,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Introductions happen only on explicit, per-provider consent.
CREATE TABLE IF NOT EXISTS intro_requests (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  plan_id      INTEGER NOT NULL REFERENCES plans(id),
  provider_id  INTEGER NOT NULL REFERENCES providers(id),
  consent_text TEXT NOT NULL,
  consented_at TEXT NOT NULL DEFAULT (datetime('now')),
  status       TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','sent','withdrawn'))
);

CREATE TABLE IF NOT EXISTS audit_log (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  at        TEXT NOT NULL DEFAULT (datetime('now')),
  actor     TEXT NOT NULL,
  action    TEXT NOT NULL,
  object    TEXT NOT NULL,
  detail    TEXT NOT NULL DEFAULT ''
);
