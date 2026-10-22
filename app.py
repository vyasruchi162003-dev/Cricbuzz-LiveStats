import streamlit as st
from utils.db_connection import initialize_database
st.set_page_config(page_title='Cricbuzz LiveStats',page_icon='🏏',layout='wide')
initialize_database()
st.sidebar.title('🏏 Cricbuzz LiveStats'); st.sidebar.caption('Cricket insights • SQL analytics • SQLite')
st.title('🏏 Cricbuzz LiveStats'); st.subheader('Real-Time Cricket Insights & SQL-Based Analytics')
st.write('A cricket analytics learning dashboard combining match and player records, SQL queries, and optional REST API integration.')
a,b,c=st.columns(3); a.metric('Core modules','4','Live • Stats • SQL • CRUD'); b.metric('SQL practice questions','25','Beginner to advanced'); c.metric('Database','SQLite','Local and portable')
st.info('Demo mode uses clearly labelled sample data. Live API access requires your own valid provider key and subscription.')
st.markdown('### Modules\n- **Live Matches:** optional live/recent API and local demo results.\n- **Top Player Stats:** batting/bowling rankings, chart and table.\n- **SQL Analytics:** 25 practice questions, result tables and CSV export.\n- **CRUD Operations:** create, read, update and delete player records.')
st.markdown('### Architecture'); st.code('Streamlit UI → API client (optional) / SQL queries → SQLite → pandas tables and Plotly charts',language='text')
st.caption('Bundled player and match values are illustrative demo data, not official Cricbuzz statistics.')
