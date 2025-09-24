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



# --- API ---
TCGPLAYER_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"


# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter - график цены
