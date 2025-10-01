import streamlit as st
import streamlit_antd_components as sac
import os
from config import DATA_DIR
from client.utils.classes.DatabaseTracker import DatabaseTracker

def render_file_tree(parquet_files=None, label="app/data", icon="table", size="sm", color="gray"):
    # --- Получаем список файлов ---
    if parquet_files is None:
        parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

    # --- Получаем текущее состояние ---
    selected_file = DatabaseTracker.get_name()
    selected_index = DatabaseTracker.get_index()

    # --- Защита от выхода за границы ---
    valid_index = None
    if selected_index is not None and 0 <= selected_index < len(parquet_files):
        valid_index = selected_index

    # --- Отрисовка дерева ---
    tree_selection = sac.tree(
        items=[sac.TreeItem(file) for file in parquet_files],
        label=label,
        icon=icon,
        size=size,
        align="start",
        open_all=True,
        checkbox=False,
        return_index=False,
        color=color,
        index=[valid_index] if valid_index is not None else []
    )

    # --- Обновление состояния при выборе ---
    if tree_selection and tree_selection != selected_file:
        DatabaseTracker.set(tree_selection, parquet_files)
        st.rerun()

    return tree_selection


