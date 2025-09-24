import streamlit as st
import pandas as pd

@st.dialog("Add new data", width="large")
def add_data(df, file_path):

    # --- DATA TYPES ---
    types = ["INT",
             "FLOAT",
             "BOOLEAN",
             "DATE",
             "TEXT"]

    new_row = {}

    for i, col in enumerate(df.columns):




        # --- ADD DATA CONTAINER ---
        add_data_container = st.container(width="stretch",
                                          horizontal=True,
                                          vertical_alignment="bottom",
                                          horizontal_alignment="distribute")

        selectbox_key = f"selectbox_{col}-{i}"
        input_key = f"input_{col}_{i}"

        col_type = df[col].dtype

        # --- INT ---
        if pd.api.types.is_integer_dtype(col_type):
            with add_data_container:
                new_row[col] = st.number_input(f"{col}", step=1, width=500, key=input_key)
                type_selectbox = st.selectbox(label="", label_visibility="collapsed", options=types, index=0, width=150, disabled=True,key=selectbox_key)

        # --- FLOAT ---
        elif pd.api.types.is_float_dtype(col_type):
            with add_data_container:
                new_row[col] = st.number_input(f"{col}", format="%.4f", width=500,key=input_key)
                type_selectbox = st.selectbox(label="", label_visibility="collapsed", options=types, index=1, width=150, disabled=True, key=selectbox_key)

        # --- BOOL ---
        elif pd.api.types.is_bool_dtype(col_type):
            with add_data_container:
                new_row[col] = st.checkbox(f"{col}", width=500,key=input_key)
                type_selectbox = st.selectbox(label="", label_visibility="collapsed", options=types, index=2, width=150, disabled=True, key=selectbox_key)

        # --- DATE ---
        elif pd.api.types.is_datetime64_any_dtype(col_type):
            with add_data_container:
                new_row[col] = st.date_input(f"{col}", width=500,key=input_key)
                type_selectbox = st.selectbox(label="", label_visibility="collapsed", options=types, index=3, width=150, disabled=True, key=selectbox_key)

        # --- TEXT ---
        else:
            with add_data_container:
                new_row[col] = st.text_input(f"{col}", width=500,key=input_key)
                type_selectbox = st.selectbox(label="", label_visibility="collapsed", options=types, index=4, width=150, disabled=True, key=selectbox_key)

    if st.button("Save data"):
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        try:
            df.to_parquet(file_path, index=False)
            st.success("New data saved")
        except Exception as e:
            st.error(f"Error: {e}")
        st.session_state["show_add_dialog"] = False
        st.rerun()
