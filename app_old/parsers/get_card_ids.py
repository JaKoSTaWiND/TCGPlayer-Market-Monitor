import requests
import pandas as pd
import os
from datetime import datetime
from app.config import TCGPLAYER_API_URL, DATA_DIR

def get_cards_productIds(game_name: str, set_value: str, max_pages: int = 10):
    safe_name = game_name.lower().replace(" ", "_").replace(":", "")
    sets_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")

    if not os.path.exists(sets_path):
        print(f"❌ Файл сетов не найден: {sets_path}")
        return

    try:
        df_sets = pd.read_parquet(sets_path)
    except Exception as e:
        print(f"❌ Ошибка при чтении parquet: {e}")
        return

    match = df_sets[df_sets["value"] == set_value]
    if match.empty:
        print(f"⚠️ Сет '{set_value}' не найден в {sets_path}")
        return

    url_value = match.iloc[0]["urlValue"]
    today = datetime.today().strftime("%d.%m.%y")

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
        "Referer": f"https://www.tcgplayer.com/search/{safe_name}/product"
    }

    base_payload = {
        "algorithm": "sales_dismax",
        "context": {
            "cart": {},
            "shippingCountry": "US",
            "userProfile": {}
        },
        "filters": {
            "term": {
                "productLineName": [game_name],
                "setName": [url_value]
            }
        },
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

    all_product_ids = []

    for page in range(max_pages):
        payload = base_payload.copy()
        payload["from"] = page * 48  # 48 карточек на страницу

        response = requests.post(TCGPLAYER_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"❌ Ошибка {response.status_code} на странице {page}")
            break

        try:
            data = response.json()
        except Exception as e:
            print(f"❌ Ошибка при парсинге JSON: {e}")
            break

        page_ids = []
        for result_block in data.get("results", []):
            for product in result_block.get("results", []):
                pid = product.get("productId")
                if pid is not None:
                    page_ids.append(int(pid))
                    all_product_ids.append(int(pid))

        print(f"✅ Страница {page + 1}/{max_pages} — получено {len(page_ids)} ID")

        if not page_ids:
            print("⚠️ Пустая страница — остановка")
            break

    new_df = pd.DataFrame({
        "productId": all_product_ids,
        "setName": set_value,
        "date": today
    })[["productId", "setName", "date"]]

    output_path = os.path.join(DATA_DIR, f"{safe_name}_product_ids.parquet")

    if os.path.exists(output_path):
        try:
            existing_df = pd.read_parquet(output_path)
        except Exception as e:
            print(f"⚠️ Ошибка при чтении существующего файла: {e}")
            existing_df = pd.DataFrame()
    else:
        existing_df = pd.DataFrame()

    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.drop_duplicates(subset="productId", keep="first", inplace=True)
    combined_df.to_parquet(output_path, index=False)

    # print(new_df)
    # print(f"✅ Добавлено {len(new_df)} productId из сета '{set_value}'")
    # print(f"📦 Всего {len(combined_df)} уникальных productId для '{game_name}' сохранено в {output_path}")
    # print(f"🔍 Собрано: {len(all_product_ids)}")

    return new_df

# get_cards_productIds("One piece card game", "Emperors in the New World")