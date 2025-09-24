import streamlit as st
import pandas as pd

@st.dialog("Add data from file", width="large")
def add_data_from_file_dialog(df, file_path):
    file_uploader = st.file_uploader(label="qqq",
                                     )