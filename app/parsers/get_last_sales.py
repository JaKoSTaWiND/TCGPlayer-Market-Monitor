import pandas as pd
import os
import asyncio
import aiohttp
import time

from config import LAST_SALES_DIR, TCGPLAYER_LAST_SALES_API_URL, DATA_DIR

# --- HEADERS ---
headers = {
    "Host": "mpapi.tcgplayer.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Origin": "https://www.tcgplayer.com",
    "Connection": "keep-alive",
    "Referer": "https://www.tcgplayer.com/",
    "Cookie": "tracking-preferences={%22version%22:1%2C%22destinations%22:{%22Actions%20Amplitude%22:true%2C%22AdWords%22:true%2C%22Google%20AdWords%20New%22:true%2C%22Google%20Enhanced%20Conversions%22:true%2C%22Google%20Tag%20Manager%22:true%2C%22Impact%20Partnership%20Cloud%22:true%2C%22Optimizely%22:true}%2C%22custom%22:{%22advertising%22:true%2C%22functional%22:true%2C%22marketingAndAnalytics%22:true}}; analytics_session_id=1760802558192; analytics_session_id.last_access=1760802679989; _gcl_au=1.1.1429207886.1755364466.2091947295.1760802568.1760802667; _ga_VS9BE2Z3GY=GS2.1.s1760802568$o35$g1$t1760802677$j30$l0$h407694816; _ga=GA1.1.1542919150.1755364468; valid=set=true; __ssid=a225eb449b24d7602f3dfa01ca4bc4b; _ga_KK8XBGNYRB=GS2.1.s1760802572$o41$g1$t1760802677$j60$l0$h0; _ga_0T2XGBC5QN=GS2.1.s1760802572$o34$g1$t1760802677$j60$l0$h0; _ga_JEQYTNS2WQ=GS2.1.s1760802572$o34$g1$t1760802677$j60$l0$h0; product-display-settings=sort=price+shipping&size=10; TCG_Data=M=1&SearchGameNameID=magic; ajs_anonymous_id=572d8c50-b316-4de6-92db-88edda4dfbd9; ajs_user_id=9c762180-cd0b-44c2-84b7-3a4ed31530be; setting=CD%3DKZ%26M%3D1; tcg-segment-session=1760802557586%257C1760802679467; TCGAuthTicket_Production=06051580AB4D74238D74734756A08B26699B63FEDA0FCC044EE91A4503BBFF7CB5A02D27C83FFA912BCE193DBE4751A1E46E44AF3185E82373E48D82E8B474FFC6242856ABDF2055E17F66B8CB9D00A1607EF2AAE933B35D836E0ED2BD6A67CCBE9A8BC0070E1025BAA20A53E7A95044B8227375; BuyerRevalidationKey=Revalidated; StoreSaveForLater_PRODUCTION=SFLK=f1e85eb0e75646c083c55781f680f4e2&Ignore=false; TCG_VisitorKey=efc79948-1968-4cf6-89e2-50d8a19a41f0; TCG_VisitorKey=5a8b7c9e-4702-403b-8d4e-91455875a01d; SearchSortSettings=M=1&ProductSortOption=BestMatch&ProductSortDesc=False&PriceSortOption=Shipping&ProductResultDisplay=grid; SellerProximity=ZipCode=&MaxSellerDistance=1000&IsActive=false",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}


# --- FETCH SINGLE PAGE ---
async def fetch_last_sales(session, game_index, setName, product_id, offset):
    api_request = {
        "conditions": [],
        "languages": [1],
        "limit": 25,
        "offset": offset,
        "listingType": "All",
        "variants": [],
        "time": int(time.time() * 1000)
    }

    url = TCGPLAYER_LAST_SALES_API_URL.format(productId=int(product_id))
    print(f"🔗 URL: {url}")

    try:
        response = await session.post(url, headers=headers, json=api_request)
        if response.status != 200:
            print(f"❌ {response.status} for productId {product_id}")
            return []

        sales_json = await response.json()
        last_sales = sales_json.get("data", [])

        sales = [
            {
                "condition": item.get("condition"),
                "variant": item.get("variant"),
                "language": item.get("language"),
                "quantity": item.get("quantity"),
                "purchasePrice": item.get("purchasePrice"),
            }
            for item in last_sales
        ]

        return sales

    except Exception as err:
        print(f"⚠️ Error for productId {product_id}: {err}")
        return []

# --- FETCH FULL SALES FOR PRODUCT ---
async def fetch_sales_for_product(session, game_index, setName, product_id, semaphore, delay):
    all_sales = []
    offset = 0

    async with semaphore:
        print(f"\n📦 Fetching sales for productId {product_id}")
        while True:
            sales = await fetch_last_sales(session, game_index, setName, product_id, offset)
            await asyncio.sleep(delay)

            if not sales:
                print(f"⚠️ No sales returned at offset {offset}")
                break

            print(f"✅ Received {len(sales)} sales at offset {offset}")
            all_sales.extend(sales)

            if len(sales) < 25:
                print(f"🛑 Less than 25 sales — stopping for productId {product_id}")
                break

            offset += 25

    save_sales_to_parquet(game_index, setName, product_id, all_sales)

    return all_sales


# --- SAVE TO PARQUET ---
def save_sales_to_parquet(game_index: str, set_name: str, product_id: int, sales: list[dict]):
    if not sales:
        print(f"⚠️ No sales to save for productId {product_id}")
        return

    # Формируем путь
    safe_game = game_index.replace(" ", "_").replace("-", "_")
    safe_set = set_name.replace(" ", "_").replace(":", "").replace("-", "_")
    folder_path = os.path.join(LAST_SALES_DIR, safe_game, safe_set)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{int(product_id)}_sales.parquet")

    # Сохраняем
    df = pd.DataFrame(sales)
    df.to_parquet(file_path, index=False)
    print(f"💾 Saved {len(df)} sales to {file_path}")


# --- MAIN COLLECTOR ---
async def collect_sales_data(game_index: str, selected_sets: list[str], batch_size: int = 10, delay: float = 1.0):
    safe_name = game_index.replace("-", "_").replace(" ", "_")
    ids_path = os.path.join(DATA_DIR, f"{safe_name}_ids.parquet")

    if not os.path.exists(ids_path):
        print(f"❌ File not found: {ids_path}")
        return

    df = pd.read_parquet(ids_path)
    if "setName" not in df.columns or "productId" not in df.columns:
        print(f"❌ Missing columns in {ids_path}")
        return

    df = df[df["setName"].isin(selected_sets)].dropna(subset=["productId"])
    product_id_to_set = dict(zip(df["productId"], df["setName"]))
    product_ids = list(product_id_to_set.keys())

    print(f"🔍 Found {len(product_ids)} productIds for sets: {selected_sets}")

    semaphore = asyncio.Semaphore(batch_size)
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            fetch_sales_for_product(session, game_index, product_id_to_set[product_id], product_id, semaphore, delay)
            for product_id in product_ids
        ]

        results = await asyncio.gather(*tasks)
        all_sales = [sale for group in results for sale in group]

        print(f"\n📊 Total sales collected: {len(all_sales)}")
        print("🧾 Sample output:")
        for i, sale in enumerate(all_sales[:5]):
            print(f"{i+1}. {sale}")

        return all_sales


# # --- ENTRY POINT ---
# if __name__ == "__main__":
#     game_index = "magic"
#     sets = ["Spellslinger Starter Kit", "Mystery Booster: Retail Exclusives"]
#     asyncio.run(collect_sales_data(game_index, sets, batch_size=5, delay=5))
