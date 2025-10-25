import asyncio
import aiohttp
import pandas as pd
import os
import math

from config import CARD_INFO_DIR, SKUS_DIR, DATA_DIR, TCGPLAYER_CARD_INFO_API_URL

BATCH_SIZE = 100

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.tcgplayer.com",
}


# --- SAVING TO PARQUET ---
def save_to_parquet(card_info_list, skus_list, game, card_dir, skus_dir):
    # --- Cards ---
    df_cards = pd.DataFrame(card_info_list)
    df_cards = df_cards[["productUrlName", "productName", "setId", "productId"]]
    cards_path = os.path.join(card_dir, f"{game}_info.parquet")

    if os.path.exists(cards_path):
        existing_cards = pd.read_parquet(cards_path)
        df_cards = pd.concat([existing_cards, df_cards], ignore_index=True).drop_duplicates()

    df_cards.to_parquet(cards_path, index=False)

    # --- SKUs ---
    df_skus = pd.DataFrame(skus_list)
    df_skus = df_skus[["productId", "sku", "condition", "variant", "language"]]

    # Добавляем setNameId из card_info
    product_to_set = {card["productId"]: card["setId"] for card in card_info_list}
    df_skus["setNameId"] = df_skus["productId"].map(product_to_set)

    skus_path = os.path.join(skus_dir, f"{game}_skus.parquet")

    if os.path.exists(skus_path):
        existing_skus = pd.read_parquet(skus_path)
        df_skus = pd.concat([existing_skus, df_skus], ignore_index=True).drop_duplicates()

    df_skus.to_parquet(skus_path, index=False)

    print(f"✅ Saved:\n- Cards → {cards_path}\n- SKUs → {skus_path}")


# --- GET productId BY CHOSEN SET ---
def get_product_ids(game_index, sets):
    safe_name = game_index.replace("-", "_").replace(" ", "_")

    sets_path = os.path.join(DATA_DIR, f"{safe_name}_sets.parquet")
    sets_df = pd.read_parquet(sets_path)

    set_column = next((col for col in ["name", "cleanSetName"] if col in sets_df.columns), None)
    if not set_column:
        raise ValueError(f"❌ No valid set name column found in {sets_path}")

    selected_sets_df = sets_df[sets_df[set_column].isin(sets)]
    selected_set_names = selected_sets_df["name"].dropna().unique().tolist()

    ids_path = os.path.join(DATA_DIR, f"{safe_name}_ids.parquet")
    cards_df = pd.read_parquet(ids_path)

    if "setName" not in cards_df.columns or "productId" not in cards_df.columns:
        raise ValueError(f"❌ Missing 'setName' or 'productId' in {ids_path}")

    filtered_cards = cards_df[cards_df["setName"].isin(selected_set_names)]
    product_ids = filtered_cards["productId"].dropna().unique().tolist()

    return product_ids, safe_name


# --- ASYNC REQUEST ---
async def fetch_single_card(session, product_id):
    url = TCGPLAYER_CARD_INFO_API_URL.format(productId=int(product_id))
    try:
        response = await session.get(url, headers=headers)
        if response.status != 200:
            print(f"❌ {response.status} for productId {product_id}")
            return None, []

        card_json = await response.json()
        skus_raw = card_json.get("skus", [])

        card_info = {
            'productUrlName': card_json.get("productUrlName"),
            'productName': card_json.get("productName"),
            'setId': card_json.get("setId"),
            'productId': product_id,
        }

        skus = [
            {
                'sku': item.get("sku"),
                'condition': item.get("condition"),
                'variant': item.get("variant"),
                'language': item.get("language"),
                'productId': product_id,
            }
            for item in skus_raw
            if item.get("sku") and item.get("condition") and item.get("variant")
        ]

        return card_info, skus

    except Exception as e:
        print(f"⚠️ Error for productId {product_id}: {e}")
        return None, []


# --- MAIN PARSING FUNC ---
async def fetch_card_info(session, game_index, sets):
    product_ids, safe_name = get_product_ids(game_index, sets)

    total = len(product_ids)
    num_batches = math.ceil(total / BATCH_SIZE)

    print(f"🔄 Fetching {total} cards in {num_batches} batches...")

    for i in range(num_batches):
        batch_ids = product_ids[i * BATCH_SIZE: (i + 1) * BATCH_SIZE]
        print(f"\n📦 Batch {i + 1}/{num_batches} — {len(batch_ids)} productIds")
        print(f"🔢 productIds: {batch_ids}")

        tasks = [fetch_single_card(session, pid) for pid in batch_ids]
        results = await asyncio.gather(*tasks)

        card_info_list = []
        skus_list_all = []

        for card_info, skus in results:
            if card_info:
                card_info_list.append(card_info)
            if skus:
                skus_list_all.extend(skus)

        print(f"✅ Parsed: {len(card_info_list)} cards, {len(skus_list_all)} SKUs")

        # Сохраняем и логируем добавленные строки
        prev_cards = 0
        prev_skus = 0

        cards_path = os.path.join(CARD_INFO_DIR, f"{safe_name}_info.parquet")
        skus_path = os.path.join(SKUS_DIR, f"{safe_name}_skus.parquet")

        if os.path.exists(cards_path):
            prev_cards = len(pd.read_parquet(cards_path))
        if os.path.exists(skus_path):
            prev_skus = len(pd.read_parquet(skus_path))

        save_to_parquet(card_info_list, skus_list_all, safe_name, CARD_INFO_DIR, SKUS_DIR)

        new_cards = len(pd.read_parquet(cards_path)) - prev_cards
        new_skus = len(pd.read_parquet(skus_path)) - prev_skus

        print(f"📥 Added to parquet: +{new_cards} cards, +{new_skus} SKUs")


async def get_card_info(game_index: str, sets: list[str]):
    async with aiohttp.ClientSession(headers=headers) as session:
        await fetch_card_info(session, game_index, sets)







# --- LAUNCH ---
# if __name__ == "__main__":
#     game_index = "magic"  # или pokemon_japan, one_piece_card_game и т.д.
#     sets = ["Commander Legends: Battle for Baldur's Gate"]
#
#     async def main():
#         async with aiohttp.ClientSession(headers=headers) as session:
#             await fetch_card_info(session, game_index, sets)
#
#     asyncio.run(main())
