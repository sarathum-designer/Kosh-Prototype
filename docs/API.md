# Kosh API

Base URL: `http://localhost:8080`. JSON in and out.

## Public

| Method | Path | What it does |
|---|---|---|
| GET | `/api/health` | `{ok, facts}` |
| GET | `/api/dataset` | Everything the front end needs: sources, published facts, cities, states with rules, conflicts, GCCs, providers, assumptions |
| GET | `/api/facts?subject=pune&metric=GCC%20count` | Filter published facts |
| GET | `/api/facts/{id}` | One fact with its source and any conflicts it belongs to |
| GET | `/api/conflicts` | Documented disagreements with explanations |
| GET | `/api/providers?category=EOR` | Providers, always alphabetical, with verified delivery counts |
| POST | `/api/compare` | Body: a plan. Returns cost ranges and incentive screens per city |
| POST | `/api/ask` | Body: `{question, plan_summary?}`. Grounded answer, retrieved fact ids, any dropped citations |
| POST | `/api/sample` | Model passthrough used by the self-hosted front end (needs `ANTHROPIC_API_KEY`) |
| POST | `/api/plans` | Save a plan; returns `{id}` |
| POST | `/api/intros` | Body: `{plan_id, providers:[names], consent}`. Fails without consent text |

Plan shape:

```json
{"company":"Acme","revenue":"100m-1b","rank":"other","functions":["engineering","data"],
 "y1":60,"y3":150,"model":"eor","cities":["bengaluru","pune"],"timeline":"Q2 2027"}
```

`model`: `eor` | `bot` | `own`. `rank`: `g2000` | `f1000` | `other`. `revenue`: `lt100m` | `100m-1b` | `gt1b`.

Compare response (abridged):

```json
{"cities":[{"city":"hyderabad",
  "cost":{"low_cr":8.151,"high_cr":11.499,"payroll_cr":7.02,"rent_cr":[0.504,0.684],"eor_cr":[0.627,3.795],
          "salary_fact":"F44","rent_fact":"F45","excludes":["fit-out","IT","recruitment fees","travel"]},
  "incentives":[{"state":"TG","verdict":"none","reasons":["No notified GCC policy to claim from today. ..."]}]}]}
```

`cost` is `null` when Kosh doesn't have the data to price a city.

## Analyst (Bearer token)

| Method | Path | What it does |
|---|---|---|
| POST | `/api/ingest` | Body: `{source:{id,publisher,title,url,date,kind,sells_services?}, text, as_of}`. Extracts candidate facts into the review queue |
| GET | `/api/review` | Pending facts |
| POST | `/api/review/{id}` | Body: `{decision:"published"|"rejected", reviewer}`. Publishing runs conflict detection and returns any conflict id |

Example:

```bash
curl -X POST localhost:8080/api/ingest -H "Authorization: Bearer dev-review-token" -H "content-type: application/json" \
  -d '{"source":{"id":"S900","publisher":"Test Wire","title":"Pune note","url":"https://example.com","date":"2026-10","kind":"news"},
       "text":"Pune now hosts 260 GCCs, the state said.","as_of":"2026-10"}'
```
