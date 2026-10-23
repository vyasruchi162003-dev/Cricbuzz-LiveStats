import streamlit as st
import pandas as pd

from api.cricbuzz_client import (
    get_live_matches,
    get_recent_matches,
    CricbuzzAPIError,
)
from utils.db_connection import get_connection


st.title("🔴 Live Matches")
st.write(
    "API requests require valid provider credentials. "
    "Local results are sample data."
)

mode = st.radio(
    "Choose view",
    ["Live API", "Recent API", "Local demo database"],
    horizontal=True,
)

if mode != "Local demo database":
    if st.button("Fetch matches", type="primary"):
        try:
            data = (
                get_live_matches()
                if mode == "Live API"
                else get_recent_matches()
            )

            # Remove the API key before displaying the response.
            if isinstance(data, dict):
                data.pop("apikey", None)

            st.json(data)
        except CricbuzzAPIError as e:
            st.warning(str(e))
            st.caption(
                "Check API key, subscription, host and current endpoint docs."
            )
else:
    with get_connection() as conn:
        df = pd.read_sql_query(
            "SELECT m.match_id,m.description,m.format,m.match_date,m.status,"
            "t1.team_name AS team_1,t2.team_name AS team_2,v.venue_name,v.city,"
            "w.team_name AS winner,m.win_margin,m.win_type "
            "FROM matches m "
            "JOIN teams t1 ON m.team1_id=t1.team_id "
            "JOIN teams t2 ON m.team2_id=t2.team_id "
            "LEFT JOIN venues v ON m.venue_id=v.venue_id "
            "LEFT JOIN teams w ON m.winner_team_id=w.team_id "
            "ORDER BY m.match_date DESC",
            conn,
        )
    st.dataframe(df, use_container_width=True, hide_index=True)
