import os

BASE_DIR = os.path.dirname(__file__)

# --- APP ---
APP_DIR = os.path.join(BASE_DIR, 'app')

DATA_DIR = os.path.join(APP_DIR, 'data')
CARD_INFO_DIR = os.path.join(DATA_DIR, 'card_info')


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
# TCGPLAYER_SETS_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
TCGPLAYER_SETS_API_URL = "https://mpapi.tcgplayer.com/v2/Catalog/SetNames?categoryId={category_id}&mpfev=4304"
TCGPLAYER_CARD_IDS_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"

# https://mpapi.tcgplayer.com/v2/Catalog/SetNames?categoryId=68&mpfev=4304 - наборы


# https://mp-search-api.tcgplayer.com/v1/search/request?q=&isList=false&mpfev=4286 - карточки в запросе

# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter - график цены
# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=annual - график цены за год

# https://mpapi.tcgplayer.com/v2/product/654455/latestsales?mpfev=4304 - прошлые продажи

# https://mp-search-api.tcgplayer.com/v2/product/643764/details?mpfev=4304 - данные по карточке
