import sys
import os
import streamlit as st
import pandas as pd


# Добавляем корень проекта (diplom/) в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.parsers.get_card_ids import get_cards_productIds
from app.parsers.see_all_ids import see_all_ids
from app.parsers.get_all_sets import get_all_sets

from app.config import DATA_DIR


st.set_page_config(
    layout="wide",
)


col1, col2 = st.columns(2)

game_options = [
    "One Piece Card Game",
    "Pokemon",
    "Pokemon Japan",
    "Magic: The Gathering",
    "Yu-Gi-Oh!"
]

set_options = []



with col1:

    col3, col4 = st.columns(2)
    col5, col6, col7 = st.columns(3)

    with col3:
        game_choice = st.selectbox(label='Game', options=game_options, index=0, key='game_option_selectbox')

    safe_name = game_choice.lower().replace(" ", "_").replace(":", "")
    file_path = os.path.join(DATA_DIR, f"{safe_name}_product_ids.parquet")
    sets_file = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")


    with col4:
        if os.path.exists(sets_file):
            try:
                df_sets = pd.read_parquet(sets_file)
                set_options = df_sets["value"].tolist()
            except Exception as e:
                st.error(f"Ошибка при загрузке сетов: {e}")
                set_options = []
        else:
            # st.warning(f"Файл сетов не найден: {sets_file}")
            set_options = []

        set_choice = st.selectbox(label='Set Name', options=set_options, index=0 if set_options else None,key='set_choice_selectbox')

    with col5:
        # Кнопка обновления наборов
        get_sets_button = st.button("Update Sets", key="get_sets_button", width="stretch")

    df_sets = pd.DataFrame()


    if get_sets_button:
        with col1:
            with st.spinner(f"Собираю sets для '{game_choice}'..."):
                df_sets = get_all_sets(game_name=game_choice)

        with col1:
            st.success(f"Найдено {len(df_sets)} наборов для {game_choice}")



    with col6:
        find_card_ids = st.button("Find Card Ids", key="find_card_ids", use_container_width=True)

    # создаём переменные вне колонок
    new_df = pd.DataFrame()
    parse_message = ""

    if find_card_ids:
        with col1:
            with st.spinner(f"Парсинг: '{game_choice}' / '{set_choice}'"):
                if set_choice:
                    new_df = get_cards_productIds(game_name=game_choice, set_value=set_choice)
                else:
                    parse_message = "⚠️ Выберите сет перед запуском парсинга."

        # после парсинга — выводим сообщения и таблицу отдельно
        with col1:

            if not set_choice:
                st.warning(parse_message)
            elif new_df is not None and not new_df.empty:
                st.success(f"Добавлено {len(new_df)} productId из сета '{set_choice}'")
            else:
                st.warning("Новых карточек не найдено или парсинг не удался.")

    with col7:
        show_all_button = st.button("Show all Ids", key="show_all_ids_button", width="stretch")


    # создаём переменную вне колонок
    df_all = pd.DataFrame()
    load_error = None

    if show_all_button:
        try:
            df_all = pd.read_parquet(file_path)
        except Exception as e:
            load_error = e

        with col1:
            if load_error:
                st.error(f"❌ Не удалось загрузить файл: {load_error}")
            else:
                st.success(f"Всего {len(df_all)} уникальных productId для '{game_choice}'")

                st.divider()
                st.text("Debug")
                st.success(f"Файл: {file_path}")


# отображение таблиц
with col2:
    if new_df is not None and not new_df.empty:
        st.caption(f"Parquet: {game_choice} | {set_choice} | productIds")
        st.dataframe(new_df, height = 800)

    if not df_all.empty:
        st.caption(f"Parquet: {game_choice}")
        st.dataframe(df_all, height = 800)

    if not df_sets.empty:
        st.caption(f"Parquet: {game_choice} | sets")
        st.dataframe(df_sets, height = 800)









