from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (DataIngestionConfig,)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

        # 🔹 Debug: Print loaded YAML
        print("DEBUG: Loaded Config =", self.config)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        # 🔹 Debug: Print values retrieved from YAML
        print(f"DEBUG: source_URL = {config.get('source_URL')}")
        print(f"DEBUG: local_data_file = {config.get('local_data_file')}")
        print(f"DEBUG: unzip_dir = {config.get('unzip_dir')}")

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config
