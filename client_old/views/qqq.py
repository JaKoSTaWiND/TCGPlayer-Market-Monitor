import streamlit as st
import pandas as pd
import os
import sys

# Подключаем корневую директорию проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.config import DATA_DIR
from client.functions.dialogs.add_data_to_parquet import add_data_to_parquet
from client.functions.dialogs.delete_data_from_parquet import delete_data_from_parquet

st.set_page_config(layout='wide')

# Получаем список всех .parquet файлов
parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

if not parquet_files:
    st.warning("В папке DATA_DIR нет .parquet файлов.")
    st.stop()

# 📁 Навбар: выбор файла + кнопки
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    selected_file = st.selectbox("📁 Выбери файл", parquet_files)

    if "last_selected_file" not in st.session_state:
        st.session_state["last_selected_file"] = selected_file
    elif st.session_state["last_selected_file"] != selected_file:
        st.session_state["last_selected_file"] = selected_file
        st.session_state["show_add_dialog"] = False
        st.session_state["show_delete_dialog"] = False

file_path = os.path.join(DATA_DIR, selected_file)

try:
    df = pd.read_parquet(file_path)
except Exception as e:
    st.error(f"❌ Ошибка при чтении файла: {e}")
    df = pd.DataFrame()





with col2:
    if st.button("➕ Добавить данные"):
        st.session_state["show_delete_dialog"] = False  # закрыть другой
        st.session_state["show_add_dialog"] = True

with col3:
    if st.button("🗑️ Удалить данные"):
        st.session_state["show_add_dialog"] = False  # закрыть другой
        st.session_state["show_delete_dialog"] = True

st.divider()




# 🧩 Диалоги
if st.session_state.get("show_add_dialog", False):
    add_data_to_parquet(df, file_path)

if st.session_state.get("show_delete_dialog", False):
    delete_data_from_parquet(df, file_path)

# 📊 Вывод таблицы
st.write(f"📦 Путь: `{file_path}`")
st.dataframe(df, use_container_width=True, height=800)
