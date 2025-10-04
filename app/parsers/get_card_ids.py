import pandas as pd
import os
import asyncio
import aiohttp
import math
import time
import streamlit as st
from streamlit import toast

from config import DATA_DIR
from config import TCGPLAYER_CARD_IDS_API_URL


# --- FETCH TO API FUNC ---
async def fetch_card_ids(session, game_index, setName, offset):

    start = time.time()

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
            # print(response.status)
            return []

        card_json = await response.json()
        card_list = card_json["results"][0]["results"]

        ids = [
            {
                "setName": item.get("setName"),
                "productId": item.get("productId")
            }
            for item in card_list
            if item.get("productId") and item.get("setName") and item.get("productLineUrlName")
        ]

        duration = time.time() - start
#         print(f"⏱ Offset {offset} completed in {duration:.2f} seconds")

        return ids

    except Exception as e:
#         print(e)
        return []


# --- INIT FUNC ---
async def get_card_ids(game_index, sets):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
    }

    safe_name = game_index.replace("-", "_").replace(" ", "_")
    sets_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")

    try:
        df_sets = pd.read_parquet(sets_path)
        df_sets = df_sets[df_sets["name"].isin(sets)]
        df_sets["releaseDate"] = pd.to_datetime(df_sets["releaseDate"], errors="coerce")
        df_sets = df_sets.sort_values("releaseDate")
        sorted_sets = df_sets["name"].tolist()
    except Exception as e:
#         print(f"❌ Failed to load or sort sets: {e}")
        sorted_sets = sets

    all_results = []

    async with aiohttp.ClientSession(headers=headers) as session:
        for setName in sorted_sets:
#             print(f"\n🔍 Parsing set: {setName}")
            st.toast(f"\n🔍 Parsing set: {setName}")

            total_count = df_sets[df_sets["name"] == setName]["count"].values[0] if "count" in df_sets.columns else 1500
#             print(f"📦 Expected cards: {total_count}")
            st.toast(f"Expected cards: {total_count}")

            num_offsets = math.ceil(total_count / 50)
            offsets = [i * 50 for i in range(num_offsets)]
            batches = [offsets[i:i + 10] for i in range(0, len(offsets), 10)]

            seen_ids = set()

            for batch_index, batch in enumerate(batches):
#                 print(f"🚀 Sending batch {batch_index + 1} with offsets: {batch}")
                st.toast(f"Sending batch {batch_index + 1} with offsets: {batch}")

                # 👇 Выводим каждый offset-запрос
                for offset in batch:
#                     print(f"🔸 Preparing request for offset {offset} in set '{setName}'")
                    start_time = time.time()

                tasks = [
                    fetch_card_ids(session, game_index, setName, offset)
                    for offset in batch
                ]
                batch_results = await asyncio.gather(*tasks)

                duration = time.time() - start_time
#                 print(f"⏱ Batch {batch_index + 1} completed in {duration:.2f} seconds")

                batch_total = 0
                for result_index, result in enumerate(batch_results):
                    if result:
                        batch_total += len(result)
                        for item in result:
                            if item["productId"] not in seen_ids:
                                item["setName"] = setName
                                all_results.append(item)
                                seen_ids.add(item["productId"])
                    else:
#                         print(f"⚠️ Empty result at offset {batch[result_index]}")
                        return

#                 print(f"✅ Parsed batch {batch_index + 1}: {batch_total} cards")
                st.toast(f"Parsed batch {batch_index + 1}: {batch_total} cards")

                await asyncio.sleep(1)

#             print(f"🎯 Total unique cards collected for {setName}: {len(seen_ids)}")
            st.toast(f"Total unique cards collected for {setName}: {len(seen_ids)}")

    df_all = pd.DataFrame(all_results)
    df_all.drop_duplicates(subset=["productId"], inplace=True)

    output_path = os.path.join(DATA_DIR, f"{safe_name}_ids.parquet")

    if os.path.exists(output_path):
        try:
            df_existing = pd.read_parquet(output_path)
#             print(f"📂 Loaded existing file with {len(df_existing)} cards")
            st.toast(f"Loaded existing file with {len(df_existing)} cards")
            df_all = pd.concat([df_existing, df_all], ignore_index=True)
            df_all.drop_duplicates(subset=["productId"], inplace=True)
        except Exception as e:
#             print(f"⚠️ Failed to load existing file: {e}")
            return []

    df_all.to_parquet(output_path, index=False)
#     print(f"\n💾 Saved total {len(df_all)} unique cards to {output_path}")
    st.toast(f"\nSaved total {len(df_all)} unique cards to {output_path}")


# if __name__ == "__main__":
#
#
#     game_index = "magic"
#     set_name = "Commander: Zendikar Rising"
#
#     asyncio.run(get_card_ids(game_index, [set_name]))
