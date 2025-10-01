import pandas as pd
import os
import asyncio
import aiohttp
import streamlit as st

from config import DATA_DIR
from config import TCGPLAYER_CARD_IDS_API_URL

async def fetch_card_ids(session, game_index, setName, offset):

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
                "setName": [setName]
            },
        },
        "from": offset,
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
        "size": 50,
        "sort": {},
    }

    try:
        response = await session.post(TCGPLAYER_CARD_IDS_API_URL, json=api_request)
        if response.status != 200:
            print(response.status)
            return []

        card_json = await response.json()
        card_list = card_json["results"][0]["results"]

        ids = [
            {
                "productLineUrlName": item.get("productLineUrlName"),
                "setName": item.get("setName"),
                "productId": item.get("productId")
            }
            for item in card_list
            if item.get("productId") and item.get("setName") and item.get("productLineUrlName")
        ]

        return ids

    except Exception as e:
        print(e)
        return []


    except Exception as e:
        print(e)

async def get_card_ids(game_index, sets):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
    }

    all_results = []

    async with aiohttp.ClientSession(headers=headers) as session:
        for setName in sets:
            offsets = [i * 50 for i in range(30)]  # 0, 50, ..., 1450

            for i in range(0, len(offsets), 10):
                batch = offsets[i:i + 10]
                tasks = [
                    fetch_card_ids(session, game_index, setName, offset)
                    for offset in batch
                ]
                batch_results = await asyncio.gather(*tasks)

                for result in batch_results:
                    if result:
                        for item in result:
                            item["setName"] = setName
                            all_results.append(item)

                # print(f"✅ Parsed {setName} batch {i // 10 + 1}")
                st.toast(f"Parsed {setName} batch {i // 10 + 1}")
                await asyncio.sleep(1)

    # --- SAVE INTO PARQUET FILE ---
    df_all = pd.DataFrame(all_results)
    safe_name = game_index.replace("-", "_").replace(" ", "_")
    output_path = os.path.join(DATA_DIR, f"{safe_name}_ids.parquet")
    df_all.to_parquet(output_path, index=False)
    # print(f"💾 Saved all sets: {len(df_all)} cards")
    # st.toast = (f"Saved all sets: {len(df_all)} cards")



# asyncio.run(get_card_ids())