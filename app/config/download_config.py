# app/config/download_config.py

import os


class DownloadConfig:
    USER_REVIEWS_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "AMAZON_FASHION.json",
    )
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    outputs_dir = os.path.join(parent_dir, "outputs")
    REDUCED_KEYWORDS_LINK_ID = "1E2dD1fArv6tFIUqT48scl3H9lfnXv9r6"
    META_PRODUCT_LINK_ID = "1TN_gGxMZMp6s2ilXdOSsQJPUhJlqynFq"
    REDUCED_KEYWORDS_PATH = rf"{outputs_dir}\reduced_keywords.json"
    META_PRODUCT_VIEW_PATH = rf"{outputs_dir}\meta_product_view.json"
