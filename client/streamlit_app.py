import streamlit as st
import sys
import os


st.set_page_config(layout="wide")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# --- PAGE SETUP ---
# dbms_page = st.Page(
#     page="views/dbms.py",
#     title="DBMS",
#     icon=":material/table_view:",
#     default=True
# )
#
# edit_table_page = st.Page(
#     page="views/custom_views/edit_table.py",
#     title="Test",
#     icon=":material/manage_search:",
# )

parsers_page = st.Page(
    page="views/parsers.py",
    title="Parsers",
    icon=":material/manage_search:",
)

pages = {
    "Database Management": [
        st.Page(
            page="views/dbms.py",
            title="DBMS",
            icon=":material/table_view:",
            default=True
        ),
        st.Page(
            page="views/edit_table.py",
            title="Test",
            icon=":material/manage_search:",
        ),
    ],
    "Parsers": [
        st.Page(
            page="views/parsers.py",
            title="Parsers",
            icon=":material/manage_search:",
        )
    ]

}

pg = st.navigation(pages, position="top")

pg.run()