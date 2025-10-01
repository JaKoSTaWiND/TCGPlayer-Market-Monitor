import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import duckdb
import urllib.parse

from config import DATA_DIR
from client.utils.classes.DatabaseTracker import DatabaseTracker
from client.utils.dialogs.add_data_dialog import add_data

# --- GET PARQUET FILES ---
parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

file_name = DatabaseTracker.get_name()
file_path = DatabaseTracker.get_path()
df = DatabaseTracker.get_df()


st.set_page_config(layout="wide")

col1, col2 = st.columns([3, 10], gap="large")

# --- COL1: FILE TREE ---
with col1:

    # # --- NAVIGATION BUTTONS ---
    # action_buttons = {0: ":material/add_box:"}
    # selection = st.segmented_control(
    #     label="",
    #     label_visibility="collapsed",
    #     options=action_buttons.keys(),
    #     format_func=lambda option: action_buttons[option],
    #     width="stretch",
    #     key="nav_selection",  # <- сохраняем выбор в session_state
    # )
    #
    #
    # # Инициализация флага показа диалога
    # if "show_add_dialog" not in st.session_state:
    #     st.session_state["show_add_dialog"] = False
    #
    # # Если пользователь только что нажал кнопку 0 — открываем диалог
    # # Важно: не сбрасываем флаг сразу после вызова add_data
    # if selection == 0 and not st.session_state["show_add_dialog"]:
    #     # Устанавливаем флаг — диалог откроется на следующем проходе рендера
    #     st.session_state["show_add_dialog"] = True
    #     # Опционально: очистить nav_selection, чтобы кнопка не считалась "нажатой" постоянно
    #     # st.session_state["nav_selection"] = None
    #
    # # Вызов диалога только если флаг выставлен (диалог сам сбросит флаг при Save/Cancel)
    # if st.session_state.get("show_add_dialog"):
    #     if df is None or file_path is None:
    #         st.error("Выберите файл в дереве, чтобы добавить запись")
    #         st.session_state["show_add_dialog"] = False
    #     else:
    #         # НЕ сбрасываем show_add_dialog здесь
    #         add_data(df, file_path)
    #
    # sac.divider(label='label', icon='house', align='center', color='gray', key="nav_divider")

    # --- FILE TREE
    selected_tree_file = sac.tree(
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

    if selected_tree_file and selected_tree_file != DatabaseTracker.get_name():
        DatabaseTracker.set(selected_tree_file)
        st.rerun()

    selected_tree_file = DatabaseTracker.get_name()
    file_path = DatabaseTracker.get_path()




# --- COL2: SQL INTERFACE ---
with col2:
    if df is not None:
        main_container = st.container(border=True, gap="small", key="main_container")

        with main_container:

            # --- SQL INPUT ---
            sql_input = st.text_area(label="", label_visibility="collapsed", height=100, key="sql_input")

            # --- SQL EXECUTION ---
            try:
                table_name = os.path.splitext(file_name)[0]
                temp_table_name = f"{table_name}_temp"
                default_sql = f"SELECT * FROM {table_name}"
                query_to_run = sql_input.strip() if sql_input.strip() else default_sql

                # Register df as view
                duckdb.register(table_name, df)

                # Drop temp table if exists
                duckdb.sql(f"DROP TABLE IF EXISTS {temp_table_name}")

                # Create temp table
                duckdb.sql(f"CREATE TEMP TABLE {temp_table_name} AS SELECT * FROM {table_name}")

                # Execute query (replace table name with temp table name)
                duckdb.sql(query_to_run.replace(table_name, temp_table_name))

                # Get updated dataframe
                updated_df = duckdb.sql(query_to_run.replace(table_name, temp_table_name)).to_df()

                # Save to parquet
                updated_df.to_parquet(file_path, index=False)

                # st.toast("Request completed")
                sac.divider(label='Dataset', icon='house', align='center', color='gray', key="dataset_divider")
                st.dataframe(updated_df, height=500)

            except Exception as e:
                st.error(f"❌ Ошибка в SQL-запросе: {e}")
