import streamlit as st
import pandas as pd

@st.dialog("🗑️ Удалить строки")
def delete_data_from_parquet(df, file_path):
    col_to_filter = st.selectbox("Столбец", df.columns)
    value_to_delete = st.text_input("Значение для удаления")

    if st.button("❌ Удалить совпадения"):
        filtered_df = df[df[col_to_filter].astype(str) == value_to_delete]
        if filtered_df.empty:
            st.warning("⚠️ Совпадений не найдено")
            return

        df = df[df[col_to_filter].astype(str) != value_to_delete]
        try:
            df.to_parquet(file_path, index=False)
            st.success(f"✅ Удалено {len(filtered_df)} строк")
        except Exception as e:
            st.error(f"❌ Ошибка при сохранении: {e}")
        st.session_state["show_delete_dialog"] = False
        st.rerun()