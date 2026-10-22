import streamlit as st, pandas as pd, plotly.express as px
from utils.db_connection import get_connection
st.title('📊 Top Player Stats')
with get_connection() as conn: players=pd.read_sql_query('SELECT p.full_name,t.team_name,p.role,p.matches,p.runs,p.wickets,p.batting_average,p.strike_rate FROM players p LEFT JOIN teams t ON p.team_id=t.team_id',conn)
a,b,c=st.columns(3); a.metric('Players',len(players)); b.metric('Sample runs',int(players.runs.sum())); c.metric('Sample wickets',int(players.wickets.sum()))
category=st.selectbox('Rank by',['Runs','Wickets','Batting average','Strike rate']); col={'Runs':'runs','Wickets':'wickets','Batting average':'batting_average','Strike rate':'strike_rate'}[category]; ranked=players.sort_values(col,ascending=False).head(10)
st.plotly_chart(px.bar(ranked,x='full_name',y=col,color='team_name',title=f'Top players by {category}'),use_container_width=True); st.dataframe(ranked,use_container_width=True,hide_index=True)
st.caption('Bundled statistics are illustrative, not verified official player records.')
