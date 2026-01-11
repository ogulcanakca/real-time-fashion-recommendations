# app/utils/choose_asin.py

import random


class ASIN_Getter:
    def get_asin(reduced_keywords, mode: str = "random"):
        if mode == "random":
            asin_keys = list(reduced_keywords.keys())
            asin = random.choice(asin_keys)
        return asin
