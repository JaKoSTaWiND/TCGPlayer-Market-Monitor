import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import urllib.parse

from config import DATA_DIR
from client.utils.classes.DatabaseTracker import DatabaseTracker

# --- GET PARQUET FILES ---
parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

file_name = DatabaseTracker.get_name()
file_path = DatabaseTracker.get_path()

df = None


col1, col2 = st.columns([3,10], gap=None)

# --- COL1: SEGMENTED BUTTONS & FILE TREE ---
with col1:

    action_buttons = {
        0: ":material/add_box:"
    }

    selection = st.segmented_control(label="",
                                     label_visibility="collapsed",
                                     options=action_buttons.keys(),
                                     format_func=lambda option: action_buttons[option],
                                     width="stretch",
                                     )

    sac.divider(label='label', icon='house', align='center', color='gray')

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

    st.write(f"`{file_path}`")
    st.write(f"`{file_name}`")

    if selected_file and selected_file != DatabaseTracker.get_name():
        # --- UPDATE SESSION STATE ---
        DatabaseTracker.set(selected_file)
        st.rerun()

    selected_file = DatabaseTracker.get_name()
    file_path = DatabaseTracker.get_path()



with col2:
    # --- MAIN CONTAINER ---
    main_container = st.container(
        border=True,
        horizontal=True,
        gap=None,
        key="main_container",
    )

    with main_container:

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

