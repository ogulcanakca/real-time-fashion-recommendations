# app/utils/find_image_url.py


class Find_URL:
    def find_image_url(product):
        if "imageURLHighRes" in product and product["imageURLHighRes"]:
            return product["imageURLHighRes"][0]
        elif "imageURL" in product and product["imageURL"]:
            return product["imageURL"][0]
        else:
            return None
