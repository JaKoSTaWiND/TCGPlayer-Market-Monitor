import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import duckdb

from config import DATA_DIR
from client.utils.classes.DatabaseTracker import DatabaseTracker
from client.utils.components.file_tree_comp import build_tree_data, extract_label_to_path

# --- SETUP ---
st.set_page_config(layout="wide")

file_name = DatabaseTracker.get_name()
file_path = DatabaseTracker.get_path()
df = DatabaseTracker.get_df()

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
        open_all=True,
        checkbox=False,
        return_index=False,
        color="gray",
    )

    # Извлекаем абсолютный путь
    if isinstance(selected_file, list):
        selected_file = selected_file[0] if selected_file else None

    label_to_path = extract_label_to_path(tree_items)
    full_path = label_to_path.get(selected_file)

    if full_path and full_path != DatabaseTracker.get_path():
        DatabaseTracker.set(full_path)
        st.rerun()

    file_name = DatabaseTracker.get_name()
    file_path = DatabaseTracker.get_path()
    df = DatabaseTracker.get_df()

# --- COL2: SQL INTERFACE ---
with col2:
    if df is not None:
        main_container = st.container(border=True, gap="small", key="main_container")

        with main_container:
            # --- SQL INPUT ---
            sql_input = st.text_area(
                label="",
                label_visibility="collapsed",
                placeholder="Введите SQL-запрос, например: SELECT * FROM df WHERE column > 100",
                height=100,
                key="sql_input"
            )

            # --- SQL EXECUTION ---
            try:
                # Автоопределение имени таблицы
                table_name = os.path.splitext(file_name)[0]
                query_to_run = sql_input.strip() if sql_input.strip() else f"SELECT * FROM {table_name}"

                # Регистрируем DataFrame как view
                duckdb.sql(f"DROP VIEW IF EXISTS {table_name}")
                duckdb.register(table_name, df)

                # Выполняем SQL-запрос
                updated_df = duckdb.sql(query_to_run).to_df()

                # Сохраняем результат
                updated_df.to_parquet(file_path, index=False)

                sac.divider(label='📊 Результат запроса', icon='database', align='center', color='gray',
                            key="dataset_divider")
                st.dataframe(updated_df, height=500)

            except Exception as e:
                st.error(f"❌ Ошибка в SQL-запросе: {e}")


