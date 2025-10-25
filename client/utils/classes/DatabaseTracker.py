import streamlit as st
import os
import pandas as pd

from config import DATA_DIR

class DatabaseTracker:

    # --- SET SESSION STATES FOR FILE NAME & FILE PATH ---
    @staticmethod
    def set(file_path):
        st.session_state["selected_file"] = os.path.basename(file_path)
        st.session_state["file_path"] = file_path  # ← сохраняем полный путь

    # --- GET FILE NAME ---
    @staticmethod
    def get_name():
        return st.session_state.get("selected_file")

    # --- GET FILE PATH ---
    @staticmethod
    def get_path():
        return st.session_state.get("file_path")

    # --- CLEAR SESSION STATES ---
    @staticmethod
    def clear():
        st.session_state["selected_file"] = None
        st.session_state["file_path"] = None

    # --- VIEW DATAFRAME ---
    @staticmethod
    def get_df():
        path = DatabaseTracker.get_path()
        if path and os.path.exists(path):
            try:
                return pd.read_parquet(path)
            except Exception as e:
                st.error(f"❌ Ошибка при чтении файла: {e}")
        return None



