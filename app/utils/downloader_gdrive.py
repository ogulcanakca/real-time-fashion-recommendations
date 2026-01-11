# app/utils/downloader_gdrive.py

import gdown
import os


class DownloaderDrive:
    def __init__(self, link_id: str, output_path: str) -> None:
        self.link_id = link_id
        self.output_path = output_path

    def download(self):
        if os.path.exists(self.output_path):
            print("File already exists at:", self.output_path)
            return

        url = f"https://drive.google.com/uc?id={self.link_id}"
        result = gdown.download(url, output=self.output_path, quiet=True, fuzzy=True)

        if result and os.path.exists(result):
            print("Download successful:", result)
        else:
            print("Download failed or file not found in specified path.")
