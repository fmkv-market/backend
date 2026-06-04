NUM_FEATURE_COLUMNS = [
    "user_cart_update_turn_rate",
    "user_click_turn_rate",
    "user_conversion_rate",
    "item_cart_update_turn_rate",
    "item_click_turn_rate",
    "item_conversion_rate",
    "u2i_cart_updates",
    "u2i_mean_time_between_cartupdates",
]

CAT_FEATURE_COLUMNS = ["product_category"]

FEATURE_COLUMNS = NUM_FEATURE_COLUMNS + CAT_FEATURE_COLUMNS

USER_FEATURE_KEYS = [
    "user_cart_update_turn_rate",
    "user_click_turn_rate",
    "user_conversion_rate",
]

ITEM_FEATURE_KEYS = [
    "item_cart_update_turn_rate",
    "item_click_turn_rate",
    "item_conversion_rate",
]

USER_ITEM_FEATURE_KEYS = [
    "u2i_cart_updates",
    "u2i_mean_time_between_cartupdates",
]

MOST_POP_ITEMS = [
    "3246920192090166857",
    "13903692426499623492",
    "10962450616201960823",
    "9080005013554695731",""
    "14450414801503444571",
    "17534690445912077162",
    "5359301700317557796",
    "8129191884521627511",
    "14589993416551700732",
    "15628079794763176260"
]