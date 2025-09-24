import streamlit as st
import pandas as pd

@st.dialog("➕ Добавить новую запись")
def add_data_to_parquet(df, file_path):
    new_row = {}
    for col in df.columns:
        col_type = df[col].dtype

        if pd.api.types.is_integer_dtype(col_type):
            new_row[col] = st.number_input(f"{col}", step=1)
        elif pd.api.types.is_float_dtype(col_type):
            new_row[col] = st.number_input(f"{col}", format="%.4f")
        elif pd.api.types.is_bool_dtype(col_type):
            new_row[col] = st.checkbox(f"{col}")
        elif pd.api.types.is_datetime64_any_dtype(col_type):
            new_row[col] = st.date_input(f"{col}")
        else:
            new_row[col] = st.text_input(f"{col}")

    if st.button("✅ Сохранить"):
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        try:
            df.to_parquet(file_path, index=False)
            st.success("✅ Запись добавлена")
        except Exception as e:
            st.error(f"❌ Ошибка при сохранении: {e}")
        st.session_state["show_add_dialog"] = False
        st.rerun()


@st.dialog("🗑️ Удалить строки")
def delete_data_dialog(df, file_path):
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

