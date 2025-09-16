import requests
import pandas as pd
import os
from app.config import TCGPLAYER_API_URL, DATA_DIR

def get_all_sets(game_name: str = "One Piece Card Game"):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
        "Referer": f"https://www.tcgplayer.com/search/{game_name.lower().replace(' ', '-')}/product"
    }

    payload = {
        "algorithm": "sales_dismax",
        "context": {
            "cart": {},
            "shippingCountry": "US",
            "userProfile": {}
        },
        "filters": {
            "term": {
                "productLineName": [game_name]
            }
        },
        "from": 0,
        "listingSearch": {
            "filters": {
                "range": {
                    "quantity": {"gte": 1}
                },
                "term": {
                    "sellerStatus": "Live"
                }
            }
        },
        "settings": {
            "useFuzzySearch": True
        },
        "size": 48,
        "sort": {
            "field": "market-price",
            "order": "desc"
        }
    }

    response = requests.post(TCGPLAYER_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"❌ Ошибка {response.status_code}")
        return

    try:
        data = response.json()
    except Exception as e:
        print(f"❌ Ошибка при парсинге JSON: {e}")
        return

    set_list = data["results"][0]["aggregations"]["setName"]
    sets = [
        {
            "urlValue": item.get("urlValue"),
            "value": item.get("value")
        }
        for item in set_list
        if item.get("urlValue") and item.get("value")
    ]

    if not sets:
        print(f"⚠️ Нет сетов для '{game_name}'")
        return

    df_sets = pd.DataFrame(sets)
    safe_name = game_name.lower().replace(" ", "_").replace(":", "")
    output_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")
    df_sets.to_parquet(output_path, index=False)

    print(df_sets)
    print(f"✅ Собрано {len(df_sets)} уникальных сетов для '{game_name}' и сохранено в {output_path}")

    return df_sets

