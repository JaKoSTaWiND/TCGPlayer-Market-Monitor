import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


# --- PAGE SETUP ---
dbms_page = st.Page(
    page="views/qqq.py",
    title="DBMS",
    default=True
)
parcer_page = st.Page(
    page="views/second.py",
    title="parcer"
)

pg = st.navigation(pages=[dbms_page, parcer_page])

pg.run()