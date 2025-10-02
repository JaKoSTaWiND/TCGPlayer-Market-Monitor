import pandas as pd
import os
import json
import asyncio
import aiohttp

from config import TCGPLAYER_SETS_API_URL
from config import DATA_DIR
from config import GAMES

async def fetch_sets_temp(session, games):

    for game_name, game_data in games.items():
        category_id = game_data["categoryId"]
        game_index = game_data["index"]

        try:
            url = TCGPLAYER_SETS_API_URL.format(category_id=category_id)
            response = await session.get(url)

            if response.status != 200:
                print("Error fetching sets")
                return

            sets_json = await response.json()

            sets_list = sets_json['results']

            sets = [
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

            df_sets = pd.DataFrame(sets)
            safe_name = game_index.replace("-", "_").replace(" ", "_")
            output_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")
            df_sets.to_parquet(output_path, index=False)

        except Exception as error:
            print("Error fetching sets")
            print(error)
            return



async def get_sets():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        await fetch_sets_temp(session, GAMES)

# asyncio.run(get_sets_temp())