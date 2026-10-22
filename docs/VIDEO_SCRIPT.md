# Seven-minute explanatory video script

Before recording, run `streamlit run app.py`, maximize the browser, close unrelated tabs, and ensure no API keys are visible. Use local demo data unless your API has already been tested. Never call demo data live.

## 0:00–0:40 — Introduction (Home page)
“Hello, my project is Cricbuzz LiveStats: Real-Time Cricket Insights and SQL-Based Analytics. The goal is to demonstrate how cricket match and player information can be organized in a relational database, queried with SQL, and presented through a Streamlit web application. The application has four main modules: match data, player statistics, SQL analytics, and player CRUD operations.”

## 0:40–1:35 — Architecture
“The interface is built with Streamlit and pandas, charts use Plotly, and SQLite stores structured data. The API client is separate and uses Python requests with environment variables for optional credentials. The database includes teams, venues, players, matches, innings, batting scores and bowling figures. Primary and foreign keys represent relationships, and indexes support common lookups. For this demo, bundled records are sample data, not official live scores.”

## 1:35–2:35 — Live Matches page
“On Live Matches, a user can choose live API data, recent API data, or the local demo database. API calls require a valid key and subscription. The fallback makes the project demonstrable without exposing credentials. The local view joins matches to both teams, venue and winner. The API client catches request failures and invalid JSON instead of crashing the app.”
**Show:** Click Live Matches, select Local demo database, point to format, date, venue, winner and margin columns.

## 2:35–3:25 — Top Player Stats
“This page summarizes the number of players, sample runs and wickets. The dropdown ranks players by runs, wickets, batting average or strike rate. A Plotly bar chart supports comparisons, and the table gives exact values. These are illustrative seed values, not official player records.”
**Show:** Change the ranking dropdown from Runs to Wickets, show chart and table.

## 3:25–4:40 — SQL Analytics
“The SQL Analytics page includes 25 practice questions at beginner, intermediate and advanced levels. It demonstrates filtering, joins, grouping, aggregation, common table expressions and window functions. I can select a question, inspect its SQL, execute it against SQLite, inspect the output and export results as CSV. Some assignment questions need toss, fielding, series or full ball-by-ball data, which the demo database does not contain.”
**Show:** Run Q1, then Q5 or Q10; point out query and result table.

## 4:40–6:05 — CRUD Operations
“The CRUD module demonstrates database maintenance. Create inserts a player after validating the name. Read lists records. Update changes selected fields using a parameterized SQL statement, and Delete requires explicit confirmation. Foreign keys help preserve integrity. Production systems should also enforce authentication and authorization for destructive actions.”
**Show:** Create a temporary “Demo Player”, update runs to 10, and optionally delete only that temporary record after confirmation. Do not delete an original sample player.

## 6:05–6:40 — Code and error handling
“Code is separated by responsibility: app.py is the entry point, pages contains each Streamlit module, api handles REST requests, utils manages database initialization, and sql contains the query registry. Credentials belong in a local environment file excluded from version control. The README contains setup instructions.”
**Show:** Briefly show `app.py`, `pages/`, `api/cricbuzz_client.py`, `utils/db_connection.py`, `sql/queries.py`, `requirements.txt`, and `README.md`. Do not show `.env`.

## 6:40–7:00 — Conclusion
“To conclude, this project demonstrates a modular cricket analytics application with a relational SQLite database, interactive visualizations, 25 SQL practice questions, player CRUD operations and optional REST API integration. Future improvements include validating the provider’s current endpoints, storing normalized live API responses, adding more historical data, access control and deployment. Thank you.”

## Recording checklist
- [ ] Screen capture and microphone enabled.
- [ ] Rehearse with a timer; target seven minutes.
- [ ] Show at least one SQL query and one CRUD action.
- [ ] Never show API keys, passwords or personal information.
- [ ] Export the actual recording as MP4 if possible and verify audio/duration.
