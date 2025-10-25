import os

BASE_DIR = os.path.dirname(__file__)

# --- APP ---
APP_DIR = os.path.join(BASE_DIR, 'app')

DATA_DIR = os.path.join(APP_DIR, 'data')
CARD_INFO_DIR = os.path.join(DATA_DIR, 'card_info')
SKUS_DIR = os.path.join(DATA_DIR, 'skus')
LAST_SALES_DIR = os.path.join(DATA_DIR, 'last_sales')


PARSERS_DIR = os.path.join(APP_DIR, 'parsers')




# --- CLIENT ---
CLIENT_DIR = os.path.join(BASE_DIR, 'client')



# --- ALL GAMES ---
GAMES = {
    "Magic: The Gathering": {
        "index": "magic",
        "categoryId": 1
    },
    "YuGiOh": {
        "index": "yugioh",
        "categoryId": 2
    },
    "Pokemon": {
        "index": "pokemon",
        "categoryId": 3
    },
    "Pokemon Japan": {
        "index": "pokemon-japan",
        "categoryId": 85
    },
    "One Piece Card Game": {
        "index": "one-piece-card-game",
        "categoryId": 68
    },
    "Disney Lorcana": {
        "index": "lorcana-tcg",
        "categoryId": 71
    },
    "Star Wars: Unlimited": {
        "index": "star-wars-unlimited",
        "categoryId": 79
    },
    "Flesh and Blood TCG": {
        "index": "flesh-and-blood-tcg",
        "categoryId": 62
    }
}



# --- API ---
TCGPLAYER_SETS_API_URL = "https://mpapi.tcgplayer.com/v2/Catalog/SetNames?categoryId={category_id}&mpfev=4304" # --- SET INFO ---
TCGPLAYER_SETS_COUNT_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request" # --- HOW MANY CARDS IN SET

TCGPLAYER_CARD_IDS_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request" # --- CARD PRODUCTID ---

TCGPLAYER_CARD_INFO_API_URL = "https://mp-search-api.tcgplayer.com/v2/product/{productId}/details?mpfev=4304" # --- CARD INFO ---

TCGPLAYER_LAST_SALES_API_URL = "https://mpapi.tcgplayer.com/v2/product/{productId}/latestsales?mpfev=4389" # --- LATEST SALES ---

# https://mpapi.tcgplayer.com/v2/Catalog/SetNames?categoryId=68&mpfev=4304 - наборы


# https://mp-search-api.tcgplayer.com/v1/search/request?q=&isList=false&mpfev=4286 - карточки в запросе

# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter - график цены
# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=annual - график цены за год

# https://mpapi.tcgplayer.com/v2/product/654455/latestsales?mpfev=4304 - прошлые продажи

    # https://mp-search-api.tcgplayer.com/v2/product/643764/details?mpfev=4304 - данные по карточке

    # https://mpgateway.tcgplayer.com/v1/pricepoints/buylist/marketprice/products/652092?mpfev=4304 - skus???
    # https://mp-search-api.tcgplayer.com/v1/product/652092/listings?mpfev=4304  - все продавцы

    # https://tcgplayer-cdn.tcgplayer.com/product/{productId}_in_1000x1000.jpg - фотка карточки

    ### не работает запрос на TCGPLAYER_LAST_SALES_API_URL хз почему
