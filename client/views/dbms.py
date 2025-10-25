import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import urllib.parse

from config import DATA_DIR
from client.utils.classes.DatabaseTracker import DatabaseTracker
from client.utils.components.file_tree_comp import build_tree_data, extract_label_to_path



file_name = DatabaseTracker.get_name()
file_path = DatabaseTracker.get_path()
df = None


# --- GET PARQUET FILES ---
parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

st.set_page_config(layout="wide")

col1, col2 = st.columns([2, 8], gap=None)

# --- COL1: FILE TREE ---
with col1:
    tree_items = build_tree_data(DATA_DIR)

    selected_file = sac.tree(
        items=tree_items,
        label="📁 Выберите файл",
        icon="table",
        size="sm",
        align="start",
        checkbox=False,
        return_index=False,
        color="gray",
    )

    # Построим словарь label → value
    label_to_path = extract_label_to_path(tree_items)
    full_path = label_to_path.get(selected_file)

    # st.write("📂 selected_file:", selected_file)
    # st.write("📂 get_path():", full_path)
    # st.write("📊 df type:", type(df))

    if isinstance(selected_file, list):
        selected_file = selected_file[0] if selected_file else None

    if full_path and full_path != DatabaseTracker.get_path():
        DatabaseTracker.set(full_path)  # ✅ сохраняем абсолютный путь
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

            if df is not None and not df.empty:
                st.dataframe(filtered_df, height=700)
            else:
                st.warning("📭 Файл пустой или не удалось загрузить данные.")

