import aiohttp
import asyncio
import pandas as pd
import os

TCGPLAYER_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
DATA_DIR = "data"  # Убедись, что папка существует или создай её вручную

# ⏱ Асинхронный запрос с задержкой
async def fetch_page(session, offset, payload_template, headers, delay=0.5):
    await asyncio.sleep(delay)  # Задержка перед каждым запросом
    payload = payload_template.copy()
    payload["from"] = offset
    try:
        async with session.post(TCGPLAYER_API_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                print(f"[{offset}] Ошибка {resp.status}: {text}")
                return {}
            return await resp.json()
    except aiohttp.ClientError as e:
        print(f"[{offset}] Ошибка сети: {e}")
        return {}

# 🚀 Основная функция парсинга
async def get_cards_productIds_async(product_line_slug: str = "one-piece-card-game", label: str = "one_piece", max_pages: int = 500, batch_size: int = 20, delay: float = 0.5):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tcgplayer.com",
        "Referer": f"https://www.tcgplayer.com/search/{product_line_slug}/product"
    }

    payload_template = {
        "algorithm": "sales_dismax",
        "context": {
            "cart": {},
            "shippingCountry": "US",
            "userProfile": {}
        },
        "filters": {
            "term": {
                "productLineName": [product_line_slug],
                "productTypeName": "Cards"
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
        "size": 24,
        "sort": {}
    }

    step = 24
    all_product_ids = set()

    async with aiohttp.ClientSession() as session:
        for batch_start in range(0, max_pages, batch_size):
            tasks = []
            for page in range(batch_start, min(batch_start + batch_size, max_pages)):
                offset = page * step
                tasks.append(fetch_page(session, offset, payload_template, headers, delay=delay))

            responses = await asyncio.gather(*tasks)

            for data in responses:
                if not data or not data.get("results") or not data["results"][0].get("results"):
                    continue

                for product in data["results"][0]["results"]:
                    pid = product.get("productId")
                    if pid is not None:
                        all_product_ids.add(int(pid))

    df = pd.DataFrame({"productId": list(all_product_ids)})
    df.drop_duplicates(inplace=True)

    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, f"{label}_product_ids.parquet")
    df.to_parquet(output_path, index=False)

    print(f"\n✅ Собрано {len(df)} уникальных productId для '{product_line_slug}'")
    print(f"📦 Сохранено в: {output_path}")
    return df, output_path

if __name__ == "__main__":
    asyncio.run(get_cards_productIds_async(
        product_line_slug="pokemon-japan",
        label="pokemon_japan",
        max_pages=100,
        batch_size=10,
        delay=10
    ))
