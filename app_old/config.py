import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


### DATA
DATA_DIR = os.path.join(BASE_DIR, 'app', 'data')

    ###SETS
ONE_PIECE_CARD_GAME_SETS_PARQUET = os.path.join(DATA_DIR, 'one_piece_card_game_sets.parquet')

    ###IDS
POKEMON_PRODUCT_IDS_PARQUET = os.path.join(DATA_DIR, 'pokemon_product_ids.parquet')
POKEMON_JAPAN_PRODUCT_IDS_PARQUET = os.path.join(DATA_DIR, 'pokemon_japan_product_ids.parquet')
ONE_PIECE_PRODUCT_IDS_PARQUET = os.path.join(DATA_DIR, 'one_piece_card_game_product_ids.parquet')




### PARSERS
PARSERS_DIR = os.path.join(BASE_DIR, 'app', 'parsers')

# components
COMPONENTS_DIR = os.path.join(PARSERS_DIR, 'components')

# URLS
TCGPLAYER_BASE_URL = 'https://www.tcgplayer.com/search/one-piece-card-game/product?productLineName=one-piece-card-game&page=1&view=grid'

# API
TCGPLAYER_API_URL = "https://mp-search-api.tcgplayer.com/v1/search/request"

# https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter - график цены


# https://mp-search-api.tcgplayer.com/v1/search/request?q=&isList=false&mpfev=4267
