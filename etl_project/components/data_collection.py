from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.entity.artifact_entity import DataCollectionArtifact
from etl_project.entity.config_entity import DataCollectionConfig

import requests
from pathlib import Path
import os
import sys
import pandas as pd

class DataCollection:
    def __init__(self, data_collection_config: DataCollectionConfig) -> None:
        try:
            self.data_collection_config = data_collection_config
        except Exception as e:
            raise ETLPipelineException(e, sys)

    def collect_data(self):
        try:
            logging.info("Started collecting the data")
            
            elo_data_resource_url   = self.data_collection_config.elo_data_resource_url
            match_data_resource_url = self.data_collection_config.match_data_resource_url

            elo_data_path   = self.data_collection_config.elo_data_file_path
            match_data_path = self.data_collection_config.match_data_file_path

            os.makedirs(Path(elo_data_path).parent, exist_ok=True)
            os.makedirs(Path(match_data_path).parent, exist_ok=True)

            if Path(elo_data_path).is_file():
               print(f"{elo_data_path} already_exists, skipping_download")
            else:
                logging.info("Downloading elo data.")
                request = requests.get(elo_data_resource_url)
                with open(elo_data_path, "wb") as f:
                   f.write(request.content)
                logging.info("Elo data download completed")
            
            if Path(match_data_path).is_file():
                print(f"{match_data_path} already exists, skipping download")
            else:
                logging.info("Downloading match data.")
                request = requests.get(match_data_resource_url)
                with open(match_data_path, "wb") as f:
                   f.write(request.content)
                logging.info("Match data download completed")
            logging.info("Data collected successfully")

            return elo_data_path, match_data_path
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
    def initiate_data_collection(self):
        try:
            elo_data_path, match_data_path = self.collect_data()
            print("Elo data path: ", elo_data_path)
            print("Match data path: ", match_data_path)
        except Exception as e:
            raise ETLPipelineException(e, sys)

        
def main():
    data_collection_config = DataCollectionConfig()
    data_collection = DataCollection(data_collection_config)
    data_collection.initiate_data_collection()

if __name__ == "__main__":
    main()