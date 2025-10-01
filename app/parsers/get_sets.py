import requests
import pandas as pd
import os
import json
import asyncio
import aiohttp
import streamlit as st

from config import TCGPLAYER_SETS_API_URL
from config import DATA_DIR
from config import GAMES

async def fetch_sets(session, game_name, game_index):
    api_request = {
                    "algorithm": "sales_dismax",
                    "context": {
                        "cart": {},
                        "shippingCountry": "US",
                        "userProfile": {}
                    },
                    "filters": {
                        "match": {},
                        "range": {},
                        "term": {
                            "productLineName": [game_index],
                        },
                    },
                    "from": 0,
                    "listingSearch": {
                        "context": {
                            "cart": {},
                        },
                        "filters": {
                            "exclude": {
                                "channelExclusion": 0,
                            },
                            "range": {
                                "quantity": {
                                    "gte": 1,
                                },
                            },
                            "term": {
                                "channelId": 0,
                                "sellerStatus": "Live",
                            },
                        },
                    },
                    "settings": {
                        "didYouMean": {},
                        "useFuzzySearch": True,
                    },
                    "size": 24,
                    "sort": {},
                }

    try:
        response = await session.post(TCGPLAYER_SETS_API_URL, json=api_request)

        if response.status != 200:
            print(f"❌ {game_name}: status {response.status}")
            return


        sets_json = await response.json()

        set_list = sets_json["results"][0]["aggregations"]["setName"]

        sets = [
                {
                    "value": item.get("value"),
                    "urlValue": item.get("urlValue")

                }
                for item in set_list
                if item.get("value") and item.get("urlValue")
            ]

        # print(DATA_DIR)
        # print(sets)
        # print(f"{game_name} {len(sets)} sets found")


        df_sets = pd.DataFrame(sets)
        safe_name = game_index.replace("-", "_").replace(" ", "_")
        output_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")
        df_sets.to_parquet(output_path, index=False)

        return game_name, len(sets)


    except Exception as e:
        print(f"Error for {game_name}: {e}")

async def get_sets():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            fetch_sets(session, game_name, game_index)
            for game_name, game_index in GAMES.items()
        ]
        results = await asyncio.gather(*tasks)

        summary_lines = "\n".join([
            f"For {game_name} found {count} sets."
            for game_name, count in results
            if game_name is not None
        ])


        return summary_lines


