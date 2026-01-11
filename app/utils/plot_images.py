# app/utils/plot_images.py

import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from app.utils.find_image_url import Find_URL


class PlotImages:
    def plot_recommendations_with_images(
        node_id, recommended_asins, meta_product_review, top_k=5
    ):
        asin_list = [node_id] + recommended_asins
        image_data = []

        for asin in asin_list:
            for i in range(len(meta_product_review)):
                if (
                    "asin" in meta_product_review[i]
                    and meta_product_review[i]["asin"] == asin
                ):
                    image_url = Find_URL.find_image_url(meta_product_review[i])
                    if image_url:
                        try:
                            response = requests.get(image_url)
                            img = Image.open(BytesIO(response.content))
                            image_data.append((asin, img))
                        except Exception as e:
                            print(f"Error loading image for ASIN {asin}: {e}")
                            image_data.append((asin, None))
                    break
            else:
                print(f"ASIN {asin} not found in meta_product_review")
                image_data.append((asin, None))

        additional_asins = recommended_asins[top_k:]
        for asin in additional_asins:
            for i in range(len(meta_product_review)):
                if (
                    "asin" in meta_product_review[i]
                    and meta_product_review[i]["asin"] == asin
                ):
                    image_url = Find_URL.find_image_url(meta_product_review[i])
                    if image_url:
                        try:
                            response = requests.get(image_url)
                            img = Image.open(BytesIO(response.content))
                            image_data.append((asin, img))
                        except Exception as e:
                            print(f"Error loading image for ASIN {asin}: {e}")
                            image_data.append((asin, None))
                    break
            else:
                print(f"ASIN {asin} not found in meta_product_review")
                image_data.append((asin, None))

        fig, axes = plt.subplots(1, min(len(image_data), top_k * 2), figsize=(20, 5))

        for ax, (asin, img) in zip(axes, image_data):
            if img is not None:
                ax.imshow(img)
                ax.set_title(f"ASIN: {asin}", pad=20)
            else:
                ax.set_title(f"ASIN: {asin}\nNo Image", pad=20)
            ax.axis("off")

        plt.subplots_adjust(wspace=0.7)

        plt.tight_layout()
        plt.savefig('output.png')
