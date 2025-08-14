from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.entity.config_entity import DataIngestionConfig
from etl_project.entity.artifact_entity import DataIngestionArtifact

import os 
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List 
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ETLPipelineException(e, sys)


    def export_collection_as_df(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], axis=1, inplace=True)
            return df
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    def export_data_into_feature_store(self, df:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_dir
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    def split_data_as_train_test_set(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                df, test_size=self.data_ingestion_config.train_test_split_ratio, 
            )
            logging.info("Train test split operation completed.")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting file paths")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info("Exported train and test file paths")
        except Exception as e:
            raise ETLPipelineException(e, sys)
    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_df()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test_set(df)


            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise ETLPipelineException(e, sys)