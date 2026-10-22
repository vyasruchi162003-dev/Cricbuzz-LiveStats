import streamlit as st, pandas as pd
from utils.db_connection import get_connection
from sql.queries import QUERIES
st.title('🧮 SQL Queries & Analytics'); st.write('Select a practice question, inspect SQL, execute it, and optionally export results.')
labels=[f"Q{i+1}. {q['title']}" for i,q in enumerate(QUERIES)]; choice=st.selectbox('Practice question',labels); item=QUERIES[labels.index(choice)]
st.markdown(f"**Level:** {item['level']} · **Purpose:** {item['purpose']}"); st.code(item['sql'],language='sql')
if st.button('Run SQL query',type='primary'):
 try:
  with get_connection() as conn: df=pd.read_sql_query(item['sql'],conn)
  st.success(f'{len(df)} rows returned'); st.dataframe(df,use_container_width=True,hide_index=True); st.download_button('Download result CSV',df.to_csv(index=False),'query_result.csv','text/csv')
 except Exception as e: st.error(f'Query failed: {e}')
st.caption('Some advanced questions require full historical, toss, fielding, series, or ball-by-ball data absent from the demo schema.')
