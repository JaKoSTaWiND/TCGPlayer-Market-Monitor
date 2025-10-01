# client/utils/dialogs/add_data_dialog.py
import streamlit as st
import pandas as pd

@st.dialog("Add new data", width="large")
def add_data(df, file_path):
    if df is None:
        st.error("No dataframe provided")
        st.session_state["show_add_dialog"] = False
        return

    # Подготовка одной пустой строки с корректными dtypes (как у тебя)
    empty_row = {}
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_integer_dtype(dtype):
            empty_row[col] = pd.Series([pd.NA], dtype="Int64")
        elif pd.api.types.is_float_dtype(dtype):
            empty_row[col] = pd.Series([pd.NA], dtype="float64")
        elif pd.api.types.is_bool_dtype(dtype):
            empty_row[col] = pd.Series([False], dtype="boolean")
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            empty_row[col] = pd.Series([pd.NaT], dtype="datetime64[ns]")
        else:
            empty_row[col] = pd.Series([""], dtype="string")
    empty_df = pd.DataFrame({k: v.values for k, v in empty_row.items()})

    st.markdown("### Add new record")
    edited = st.data_editor(empty_df, num_rows="fixed", use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save data"):
            try:
                new_row = edited.iloc[0:1].copy()
                # приведение типов как у тебя...
                for col in new_row.columns:
                    target_dtype = df[col].dtype
                    if pd.api.types.is_integer_dtype(target_dtype):
                        new_row[col] = new_row[col].astype("Int64")
                    elif pd.api.types.is_float_dtype(target_dtype):
                        new_row[col] = pd.to_numeric(new_row[col], errors="coerce").astype("float64")
                    elif pd.api.types.is_bool_dtype(target_dtype):
                        new_row[col] = new_row[col].astype("boolean")
                    elif pd.api.types.is_datetime64_any_dtype(target_dtype):
                        new_row[col] = pd.to_datetime(new_row[col], errors="coerce")
                    else:
                        new_row[col] = new_row[col].astype("string")

                result_df = pd.concat([df, new_row], ignore_index=True, sort=False)
                result_df.to_parquet(file_path, index=False)

                # Сбрасываем флаг и перезапускаем — диалог закроется
                st.rerun()

            except Exception as e:
                st.error(f"Error while saving new row: {e}")

