import os

BASE_DIR = os.path.dirname(__file__)

# --- APP ---
APP_DIR = os.path.join(BASE_DIR, 'app')

DATA_DIR = os.path.join(APP_DIR, 'data')
PARSERS_DIR = os.path.join(APP_DIR, 'parsers')



# --- CLIENT ---

# --- URLS ---

LOCALHOST_URL = "http://localhost:8501/"
EDIT_TABLE_URL = LOCALHOST_URL + "edit_table/"

CLIENT_DIR = os.path.join(BASE_DIR, 'client')



# --- ALL GAMES ---
GAMES = {
    "Magic: The Gathering": "magic",
    "YuGiOh": "yugioh",
    "Pokemon": "pokemon",
    "Pokemon Japan": "pokemon-japan",
    "One Piece Card Game": "one-piece-card-game",
    "Disney Lorcana": "lorcana-tcg",
    "Star Wars: Unlimited": "star-wars-unlimited",
    "Flesh and Blood TCG": "flesh-and-blood-tcg"
}


# --- API ---
TCGPLAYER_SETS_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"
TCGPLAYER_CARD_IDS_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"


# https://mp-search-api.tcgplayer.com/v1/search/request?q=&isList=false&mpfev=4286 - карточки в запросе

# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter - график цены
# в - график цены за год

# https://mpapi.tcgplayer.com/v2/product/654455/latestsales?mpfev=4304 - прошлые продажи
