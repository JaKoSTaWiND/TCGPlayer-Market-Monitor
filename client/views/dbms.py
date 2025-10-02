import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import urllib.parse

from config import DATA_DIR
from config import EDIT_TABLE_URL
from client.utils.classes.DatabaseTracker import DatabaseTracker
from client.utils.dialogs.add_data_dialog import add_data
from client.utils.dialogs.add_data_from_file_dialog import add_data_from_file_dialog


file_name = DatabaseTracker.get_name()
file_path = DatabaseTracker.get_path()
df = None


# --- GET PARQUET FILES ---
parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

st.set_page_config(layout="wide")

col1, col2 = st.columns([2, 8], gap=None)

# --- COL1: FILE TREE ---
with col1:
    selected_file = sac.tree(
        items=[sac.TreeItem(file) for file in parquet_files],
        label="app/data",
        icon="table",
        size="sm",
        align="start",
        open_all=True,
        checkbox=False,
        return_index=False,
        color="gray",
    )
    st.write(f"`file_path: {file_path}`")
    st.write(f"`selected_file: {file_name}`")

    if selected_file and selected_file != DatabaseTracker.get_name():
        DatabaseTracker.set(selected_file)
        st.rerun()
    file_name = DatabaseTracker.get_name()
    file_path = DatabaseTracker.get_path()



    df = DatabaseTracker.get_df()


# --- COL2: NAVBAR & TABLE ---
if df is not None:
    with col2:

        # --- NAVBAR ---
        nav_container = st.container(
            border=True,
            width="stretch",
            horizontal=True,
            gap="small",
            horizontal_alignment="center",
            vertical_alignment="bottom",
            key="nav_container",
        )

        with nav_container:
            search_input = st.text_input(
                label="",
                label_visibility="collapsed",
                placeholder="Search...",
                icon=":material/search:",
                key="search_input"
            )

            button_width = 100

            go_to_edit_page_button = st.button(
                label="",
                icon=":material/table_edit:",
                width=button_width,
                key="go_to_edit_page_button"
            )

            if go_to_edit_page_button and file_path:
                st.switch_page("views/edit_table.py")

        # --- TABLE ---
        dataframe_container = st.container(
            width="stretch",
            height="content",
            horizontal_alignment="center",
            key="dataframe_container"
        )


        with dataframe_container:
            query = search_input
            if query:
                filtered_df = df[df.apply(lambda row: row.map(str).str.contains(query, regex=False).any(), axis=1)]
            else:
                filtered_df = df

            st.dataframe(filtered_df, height=700)
