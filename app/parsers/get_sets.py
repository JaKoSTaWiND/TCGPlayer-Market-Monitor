import pandas as pd
import os
import json
import asyncio
import aiohttp
import re

from config import TCGPLAYER_SETS_API_URL
from config import TCGPLAYER_SETS_COUNT_API_URL
from config import DATA_DIR
from config import GAMES

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.tcgplayer.com",
}

# --- SETS BASE INFO
async def fetch_sets_info_temp(session, games):
    all_sets = []

    for game_name, game_data in games.items():
        category_id = game_data["categoryId"]

        try:
            url = TCGPLAYER_SETS_API_URL.format(category_id=category_id)
            response = await session.get(url)

            if response.status != 200:
                print(f"Error fetching sets for {game_name}")
                continue

            sets_json = await response.json()
            sets_list = sets_json['results']

            sets_data = [
                {
                    'setNameId': item.get('setNameId'),
                    'name': item.get('name'),
                    'cleanSetName': item.get('cleanSetName'),
                    'urlName': item.get('urlName'),
                    'abbreviation': item.get('abbreviation'),
                    'releaseDate': item.get('releaseDate'),
                }
                for item in sets_list
            ]

            all_sets.extend(sets_data)

        except Exception as error:
            print(f"Error fetching sets for {game_name}")
            print(error)

    return pd.DataFrame(all_sets)


# --- SETS CARD COUNT ---
async def fetch_sets_card_count(session, games):

    for game_name, game_data in games.items():
        game_index = game_data["index"]

        # --- API REQUEST
        api_request = {
          "algorithm": "sales_dismax",
          "context": {
            "cart": {},
            "shippingCountry": "US",
          },
          "filters": {
            "term": {
              "productLineName": [game_index],
            },
            "range": {},
            "match": {}
          },
          "from": 0,
          "listingSearch": {
            "context": {
              "cart": {}
            },
            "filters": {
              "term": {
                "sellerStatus": "Live",
                "channelId": 0
              },
              "range": {
                "quantity": {
                  "gte": 1
                }
              },
              "exclude": {
                "channelExclusion": 0
              }
            }
          },
          "settings": {
            "useFuzzySearch": True,
            "didYouMean": {}
          },
          "size": 24,
          "sort": {}
        }

        try:
            response = await session.post(TCGPLAYER_SETS_COUNT_API_URL, json=api_request)

            if response.status != 200:
                print("Error fetching sets")
                return

            sets_json = await response.json()

            sets_list = sets_json['results'][0]['aggregations']['setName']

            sets_data = [
                {
                    'urlValue': item.get('urlValue'),
                    'count': item.get('count'),
                }
                for item in sets_list
            ]

            df_count = pd.DataFrame(sets_data)

            return df_count

        except Exception as error:
            print("Error fetching sets")
            print(error)
            return


# --- MERGE DATAFRAMES AND SAVE THEM TO PARQUET ---
def df_merge_and_save(df_info, df_count, game_name):
    df_merged = pd.merge(df_info, df_count, left_on="urlName", right_on="urlValue", how="inner")

    game_index = GAMES[game_name]["index"]
    safe_name = game_index.replace("-", "_").replace(" ", "_")
    output_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")

    df_merged.to_parquet(output_path, index=False)
    print(f"✅ Saved {len(df_merged)} sets for {game_name} → {output_path}")

    return df_merged

# --- CREATE REQUEST FOR ONE GAME AND SAVE TO PARQUET DUE TO df_merge_and_save ---
async def process_game(session, game_name, game_data):
    print(f"🔍 Fetching sets for {game_name}...")

    df_info = await fetch_sets_info_temp(session, {game_name: game_data})
    df_count = await fetch_sets_card_count(session, {game_name: game_data})

    if df_info is not None and df_count is not None:
        df_merge_and_save(df_info, df_count, game_name)

    else:
        print(f"Skipped {game_name} due to missing data")




# --- MAKE A LOOP FOR GAMES FOR process_game TO CREATE REQUESTS FOR ALL GAMES ---
async def get_sets():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            process_game(session, game_name, game_data)
            for game_name, game_data in GAMES.items()
        ]
        await asyncio.gather(*tasks)






