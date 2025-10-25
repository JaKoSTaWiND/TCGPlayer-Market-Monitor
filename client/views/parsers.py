import streamlit as st
import streamlit_antd_components as sac
import os
import pandas as pd
import asyncio

from config import DATA_DIR
from config import GAMES

from app.parsers.get_sets import get_sets
from app.parsers.get_card_ids import get_card_ids
from app.parsers.get_card_info import get_card_info
from app.parsers.get_last_sales import collect_sales_data

st.set_page_config(layout="wide")


# --- NAVBAR ---
# --- UPDATE SETS BUTTON ---
update_sets_button = st.button("Update sets", key="update_sets_button")

if update_sets_button:
    asyncio.run(get_sets())
    st.toast("Complite")

sac.divider(label='label', icon='house', align='center', color='gray', key="nav_divider")


# --- GET CARD IDS CONTAINER ---
get_card_ids_container = st.container(border=True,
                                      gap="small",
                                      vertical_alignment="center",
                                      key="get_card_ids_container")




with get_card_ids_container:

    settings_container = st.container(border=True,
                                      gap="small",
                                      horizontal=True,
                                      vertical_alignment="center",
                                      key="settings_container")

    buttons_container = st.container(border=True,
                                      gap="small",
                                      horizontal=True,
                                      vertical_alignment="center",
                                      key="buttons_container")

    with settings_container:
        # --- GAME SELECTOR ---
        game_selection = st.selectbox(
            label="",
            label_visibility="collapsed",
            options=list(GAMES.keys()),
            width=300,
            key="game_selection"
        )

        # --- FILTER BY CHOSEN GAME ---
        game_index = GAMES[game_selection]["index"]
        safe_game_index = game_index.replace("-", "_").replace(" ", "_")
        parquet_filename = f"{safe_game_index}_sets.parquet"
        parquet_path = os.path.join(DATA_DIR, parquet_filename)

        try:
            df_sets = pd.read_parquet(parquet_path)
            available_sets = df_sets["name"].tolist()
        except Exception as e:
            # st.error(f"❌ Не удалось загрузить наборы для {game_selection}: {e}")
            st.toast("No sets")
            st.toast(f"{e}")
            available_sets = []


        # --- SETS SELECTOR ---
        choose_all_sets = False
        sets_selection = st.multiselect(
            label="",
            label_visibility="collapsed",
            options=available_sets,
            width="stretch",
            disabled=st.session_state.get("choose_all_sets", False),
            key="sets_selection"
        )

        # --- ALL SETS CHECKBOX ---
        choose_all_sets = st.checkbox(label="All sets", key="choose_all_sets")


    with buttons_container:

        # --- GET CARD IDS BUTTON ---
        get_card_ids_button  = st.button("Get card Ids", width=300,key="get_card_ids_button")
        get_card_info_button = st.button("Get card info", width=300, key="get_card_info_button")
        get_last_sales_button = st.button("Get last sale", width=300, key="get_last_sales_button")


    # --- get_card_ids_button LOGIC ---
    if get_card_ids_button:
        selected_sets = available_sets if st.session_state.get("choose_all_sets", False) else st.session_state.get("sets_selection", [])
        st.write(selected_sets)

        if not selected_sets:
            st.toast("Choose one set")
        else:
            asyncio.run(get_card_ids(game_index, selected_sets))
            st.toast("Parsing complited")


    # get_card_info_button LOGIC ---
    if get_card_info_button:
        selected_sets = available_sets if st.session_state.get("choose_all_sets", False) else st.session_state.get("sets_selection", [])
        st.write(selected_sets)

        if not selected_sets:
            st.toast("Choose one set")
        else:
            asyncio.run(get_card_info(game_index, selected_sets))
            st.toast("Parsing complited")

    # get_last_sales_button LOGIC ---
    if get_last_sales_button:
        selected_sets = available_sets if st.session_state.get("choose_all_sets", False) else st.session_state.get(
            "sets_selection", [])
        st.write(selected_sets)

        if not selected_sets:
            st.toast("Choose one set")
        else:
            asyncio.run(collect_sales_data(game_index, selected_sets))
            st.toast("Parsing complited")

sac.divider(label='label', icon='house', align='center', color='gray', key="get_card_ids_divider")



# # --- GET CARD INFO CONTAINER ---
# get_card_info_container = st.container(border=True,
#                                       gap="small",
#                                       horizontal=True,
#                                       vertical_alignment="center",
#                                       key="get_card_info_container")

# with get_card_info_container:
#
#     # col1, col2, col3, col4, col5, col6  = st.columns(6, border=True, gap=None)
#
#
#
#     # --- GAME SELECTOR ---
#     game_selection_card_info = st.selectbox(
#         label="",
#         label_visibility="collapsed",
#         options=list(GAMES.keys()),
#         width=300,
#         key="game_selection_card_info"
#     )
#
#
#
#     # --- FILTER BY CHOSEN GAME ---
#     game_index = GAMES[game_selection_card_info]["index"]
#     safe_game_index = game_index.replace("-", "_").replace(" ", "_")
#     parquet_filename = f"{safe_game_index}_sets.parquet"
#     parquet_path = os.path.join(DATA_DIR, parquet_filename)
#
#     choose_all_cards = False
#     cards_selection = st.multiselect(
#         label="",
#         label_visibility="collapsed",
#         options=available_sets,
#         width=500,
#         disabled=st.session_state.get("choose_all_cards", False),
#         key="cards_selection"
#     )
#
#
#
#     # --- ALL SETS CHECKBOX ---
#     choose_all_sets = st.checkbox(label="All sets", width="stretch", key="choose_all_cards")