# Cricbuzz LiveStats — Real-Time Cricket Insights & SQL-Based Analytics

Streamlit educational project demonstrating cricket dashboards, SQLite relational design, SQL analytics, player CRUD and optional Cricbuzz-compatible REST API access.

**Data honesty:** bundled records are illustrative sample/demo data, not official or live Cricbuzz statistics. Live API access depends on your own provider subscription, API key and current endpoint documentation.

## Features
- Home page and architecture overview.
- Live/recent match API request UI with error handling and local demo fallback.
- Top player statistics with Plotly chart and table.
- 25 SQL practice questions across beginner, intermediate and advanced levels.
- Player create/read/update/delete with parameterized SQL.
- SQLite tables for teams, venues, players, matches, innings, batting scores and bowling figures; constraints, foreign keys and indexes.
- Requirements, `.env.example`, test cases, video script and checklist.

## Run locally
1. Install Python 3.10+.
2. Extract the ZIP and open a terminal in `Cricbuzz_LiveStats`.
3. Create environment: `python -m venv .venv`
4. Activate: Windows `.venv\\Scripts\\activate`; macOS/Linux `source .venv/bin/activate`.
5. Install: `pip install -r requirements.txt`
6. Run: `streamlit run app.py`
7. Open the local URL printed by Streamlit (usually `http://localhost:8501`).

Database and demo data are initialized automatically in `data/cricbuzz.db`.

## Optional API setup
Copy `.env.example` to `.env`, add your own API key and confirm the current provider host/endpoints. API endpoints may need adaptation for your subscription. Never share or commit `.env`. The dashboard works in demo mode without credentials.

## Structure
- `app.py`: home page and app initialization
- `pages/`: live matches, player stats, SQL analytics, CRUD
- `api/cricbuzz_client.py`: REST API requests and error handling
- `utils/db_connection.py`: database connection, schema, seed records
- `sql/queries.py`: 25 SQL questions
- `sql/schema.sql`: schema note; canonical schema is in `utils/db_connection.py`
- `tests/`: basic database tests
- `docs/`: video script and checklist

## Relationships
Teams have many players and matches; venues host matches; matches contain innings; innings contain batting and bowling records. Foreign keys maintain referential integrity. Indexes support date, format, team and player lookups.

## Tests
Run `pytest -q`. Optional database check: `python -c "from utils.db_connection import initialize_database; initialize_database(); print('Database initialized')"`.

## Limitations
This is a functional educational prototype, not a production live-score service. Sample player values are illustrative. Some advanced SQL tasks require toss, fielding, series and complete ball-by-ball/history data not present in the demo schema. API routes vary by provider. Future work: normalize API payloads into SQL, add caching, auth/authorization, richer historical data and deployment secrets.
