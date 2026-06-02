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
