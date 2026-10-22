import streamlit as st, pandas as pd
from utils.db_connection import get_connection
st.title('🛠️ Player CRUD Operations'); st.write('Changes persist in the local SQLite database.')
with get_connection() as conn:
 teams=pd.read_sql_query('SELECT team_id,team_name FROM teams ORDER BY team_name',conn); players=pd.read_sql_query('SELECT player_id,full_name,team_id,role,batting_style,bowling_style,matches,runs,wickets,batting_average,strike_rate FROM players ORDER BY player_id',conn)
st.subheader('Read — current players'); st.dataframe(players,use_container_width=True,hide_index=True); opts={r.team_name:int(r.team_id) for r in teams.itertuples()}
with st.expander('Create a player'):
 with st.form('create_player'):
  name=st.text_input('Full name'); team=st.selectbox('Team',list(opts)); role=st.selectbox('Role',['Batsman','Bowler','All-rounder','Wicket-keeper']); bat=st.text_input('Batting style','Right-hand'); bowl=st.text_input('Bowling style','Not applicable'); runs=st.number_input('Career runs',0,100000,0); wickets=st.number_input('Career wickets',0,2000,0); submit=st.form_submit_button('Create player')
  if submit:
   if not name.strip(): st.error('Full name is required.')
   else:
    with get_connection() as conn: conn.execute('INSERT INTO players(full_name,team_id,role,batting_style,bowling_style,runs,wickets) VALUES(?,?,?,?,?,?,?)',(name.strip(),opts[team],role,bat,bowl,runs,wickets))
    st.success('Created.'); st.rerun()
if not players.empty:
 ids=players.player_id.astype(int).tolist()
 with st.expander('Update player'):
  pid=st.selectbox('Player ID',ids,key='upd'); row=players[players.player_id==pid].iloc[0]
  with st.form('update_player'):
   nm=st.text_input('Name',str(row.full_name)); role2=st.selectbox('Role',['Batsman','Bowler','All-rounder','Wicket-keeper'],index=['Batsman','Bowler','All-rounder','Wicket-keeper'].index(row.role)); runs2=st.number_input('Runs',0,100000,int(row.runs)); wk2=st.number_input('Wickets',0,2000,int(row.wickets)); go=st.form_submit_button('Save update')
   if go:
    if not nm.strip(): st.error('Name required.')
    else:
     with get_connection() as conn: conn.execute('UPDATE players SET full_name=?,role=?,runs=?,wickets=? WHERE player_id=?',(nm.strip(),role2,runs2,wk2,int(pid)))
     st.success('Updated.'); st.rerun()
 with st.expander('Delete player'):
  did=st.selectbox('Player ID to delete',ids,key='del'); confirm=st.checkbox('Confirm permanent deletion')
  if st.button('Delete selected player',disabled=not confirm):
   with get_connection() as conn: conn.execute('DELETE FROM players WHERE player_id=?',(int(did),))
   st.success('Deleted.'); st.rerun()
