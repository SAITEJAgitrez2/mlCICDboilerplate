import os
import urllib.request as request
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size
import shutil
import subprocess
from pathlib import Path
from textSummarizer.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """Downloads a file from the given URL if it does not already exist."""
        local_file = Path(self.config.local_data_file)

        if local_file.exists() and local_file.stat().st_size > 0:
            logger.info(f"File already exists: {local_file} ({get_size(local_file)})")
            return

        # 🔹 Check if `source_URL` is empty
        if not self.config.source_URL or self.config.source_URL.strip() == "":
            raise ValueError("source_URL is missing or empty in config.yaml")

        try:
            logger.info(f"Downloading file from {self.config.source_URL} ...")

            # 🔹 Debug print before download
            print(f"DEBUG: Attempting to download from {self.config.source_URL}")
            print(f"DEBUG: Saving to {local_file}")

            # 🔹 Open a request to the URL
            with request.urlopen(self.config.source_URL) as response:
                print(f"DEBUG: HTTP Response Code = {response.status}")
                if response.status != 200:
                    raise Exception(f"HTTP Error: {response.status} while downloading {self.config.source_URL}")

                # 🔹 Save the file
                with open(local_file, "wb") as out_file:
                    shutil.copyfileobj(response, out_file)

            # 🔹 Verify file size after download
            print(f"DEBUG: Downloaded file size = {local_file.stat().st_size} bytes")
            if local_file.stat().st_size == 0:
                raise Exception(f"Download failed: File is empty after downloading {self.config.source_URL}")

            logger.info(f"Download complete: {local_file} ({get_size(local_file)})")

        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise Exception(f"Failed to download {self.config.source_URL}: {e}")
    def extract_zip_file(self):
        """Extract ZIP file using system tar command, with better error handling."""
        unzip_path = Path(self.config.unzip_dir)
        os.makedirs(unzip_path, exist_ok=True)
        local_zip = Path(self.config.local_data_file)

        if not local_zip.exists():
            raise FileNotFoundError(f"File not found: {local_zip}")

        try:
            logger.info(f"Extracting ZIP file using system `tar` command to {unzip_path} ...")

            # Run tar, but capture errors without stopping execution
            result = subprocess.run(
                ["tar", "-xf", str(local_zip), "-C", str(unzip_path)],
                capture_output=True,
                text=True
            )

            # 🔹 If tar returned an error but extracted files, ignore the error
            if result.returncode != 0:
                if any(Path(unzip_path).iterdir()):  # Check if files were extracted
                    logger.warning(f"Extraction completed with warnings: {result.stderr}")
                else:
                    raise ValueError(f"Extraction failed: {result.stderr}")

            logger.info(f"Extraction complete using system tar command.")

        except Exception as e:
            raise ValueError(f"Extraction failed: {e}")